# Neu.ro Airflow plugin

This package helps you execute your ML workloads on [neu.ro](https://neu.ro/) platform from Airflow environment.

Also, take a look at our [CLI reference](https://docs.neu.ro/references/cli-reference) and [Python API reference](https://neuromation-sdk.readthedocs.io/en/latest/).

## Environment
- Python 3.6+
- apache-airflow >= 1.10.x
- Neuromation >= 20.4.6

## Installation

The plugin is written to automatically register with Airflow, so all you have to do is install it into your Python environment:

```
pip install neuro-airflow-plugin
```

## Usage

Before start you need to get a Neuro token by using CLI command:

```
neuro config show-token
```

and set up a Neuro Connection (`neuro_default` by default) in Airflow:

```
airflow connections --add \
    --conn_id neuro_default2 \
    --conn_type "neuro" \
    --conn_extra '{"token": "Put your Token here..."}'
```

Apart from `token` you can also provide those fields as part of extra json:

* `cluster` - name of the cluster used for compute scheduling. Default cluster will be used if not provided.
* `api_url` - entry URL for Neuro Platform. Only needed for custom clusters.

You can set up the connection from UI interface as well, just put the same JSON document
into `Extra` form field. Connection type does not matter, so you can pick any that the UI allows.

For more information on how to set up connections in Airflow see
[Managing Connections](https://airflow.apache.org/docs/stable/howto/connection/index.html).

### NeuroRunOperator

Runs a Job in the Neuro Platform. Example usage:

```python
from airflow.operators.neuro import NeuroRunOperator


run = NeuroRunOperator(
    task_id="small-deeds",

    job_command="echo 'Big things start from small deeds'",
    job_image="ubuntu:{{ var.value.ubuntu_tag }}",
    job_resources_preset="{% if var.value.use_large_cpu %}cpu-large{% else %}cpu-small{% endif %}"
)
```

For more usage examples see `examples/dags` folder of the repository.

**Operator arguments**

* `job_command` **str** *Required* - Command to be executed in the Job. If you need to override the
  entrypoint of an image, see `job_entrypoint` instead.
* `job_image` **str** *Required* - Container image used for the Job. Name can be either a docker image
  name hosted on an external public repository or a Neuro image specified by `image://` scheme.
* `job_name` **str** - Optional job name. Note that creating 2 running jobs with the same name by the
  same user is forbidden.
* `job_volumes` **list** - List of strings describing a volume mount or `neuromation.Volume` objects.
  String description consists of 3 parts separated by column: *storage URI*, *mount path*, *mount mode*.
  For example: `storage:my-project:/var/storage:ro`.
* `job_resources_preset` **str** - Predefined resource configuration (to see available values, run `neuro config show`)
* `job_resources` **Resources** - Custom resource configuration. See
  [Python API reference](https://neuromation-sdk.readthedocs.io/en/latest/jobs_reference.html#resources)
  for details.
* `job_is_preemptible` **bool** - Whether the Job may be run on a preemptible, or also known as Spot instance.
  Is only used with custom resource configuration.
* `job_extshm` **bool** - Request extended '/dev/shm' space. Defaults to `True` and is only used with
  predefined resource configuration.
* `job_tags` **list** - List of string tags to mark the Job with. Can later be used for filtering, etc.
* `job_description` **str** - Optional job description in free format.
* `job_lifespan` **float** - Optional job run-time limit in seconds. Is unlimited by default.
* `job_environ` **dict** - Environment variables to run the Job with. Jinja template support is only provided for values,
  not for keys, see more details below.
* `job_entrypoint` **str** - Override ENTRYPOINT of the container image.
* `job_http_port` **str** - Enable HTTP port forwarding to specified container port. If used you can access it from
  a custom link definition on the Task panel in Airflow UI (see
  [Airflow docs](https://airflow.apache.org/docs/stable/howto/define_extra_link.html?highlight=link)
  for details on how it works). Disabled by default.
* `job_http_auth` **bool** - Disable Neuro authentication on the exposed port in `job_http_port`.
* `job_tty` **bool** - Allocate a TTY for the Container.
* `job_detach` **bool** - Detach after starting the job. If detached Job logs will not be viewable in Airflow interface,
  but the job will not consume Airflow worker slot. Defaults to `True`.
* `raise_on_errno` **bool** - Raise an error if job returns a non-zero exit code. Ignored if `job_detach` is `True`. Default to `True`.
* `neuro_conn_id` **bool** - Name of the connection to use for Neuro authentication. Defaults to `neuro_default`.

See also the `neuro run` reference in [CLI documentation](https://docs.neu.ro/references/cli-reference/job#run)

**Jinja2 template fields**

Airflow supports passing custom attributes and dynamic definitions using Jinja templating fields. This operator
supports templating on the following fields:

* `job_command`
* `job_image`
* `job_volumes`
* `job_name`
* `job_resources_preset`
* `job_tags`
* `job_environ`
* `job_entrypoint`
* `job_description`
* `job_http_port`
* `neuro_conn_id`

**XCom exports**

The operator exports 2 XCom values: `return_value` (default in Airflow for query) and `assigned_job`. Both are
JSON documents with the following fields:

* `id` **str** - Job ID assigned by Neuro on start.
* `exit_code` **int** - Command return code if the Job already finished.
* `status` *str* - One of job statuses: `pending`, `running`, `succeeded`, `failed` or `unknown`.
* `http_url` *str* - URL of the exposed HTTP port if `job_http_port` is used.

### NeuroJobStatusSensor

Wait for a Job to be completed or any other status transition to happen. Example usage:

```python
from airflow.sensors.neuro import NeuroJobStatusSensor


wait = NeuroJobStatusSensor(
    task_id="wait_close",
    job_id="{{ task_instance.xcom_pull(task_ids='small-deeds')['id'] }}",  # noqa
    poke_interval=5,
    timeout=10 * 60,
)
```

**Operator arguments**

* `job_id` **str** - Job ID to query for status updates.
* `job_statuses` **list** - List
  [JobStatus](https://neuromation-sdk.readthedocs.io/en/latest/jobs_reference.html#jobstatus)
  enum values to wait for.
* `neuro_conn_id` **str** - Name of the connection to use for Neuro authentication. Defaults to `neuro_default`.

**Jinja2 template fields**

* `job_id`

**XCom exports**

Does not export any XCom values.


### NeuroHook

In some cases you may need to access other functionalities of the platform. This can be done using the NeuroHook.
For example:

```python
import yarl
from neuromation.api import ResourceNotFound

from airflow.hooks.neuro import NeuroHook
from airflow.operators.python_operator import BranchPythonOperator


def check_model(templates_dict, **kw):
    hook = NeuroHook()
    with hook:
        try:
            hook.run(
                hook.client.storage.stat(
                    yarl.URL("storage:" + templates_dict["model_path"])
                )
            )
            return "process_with_model"
        except ResourceNotFound:
            return "process_without_model"


check_model = BranchPythonOperator(
    task_id="check_model_exists",
    python_callable=check_model,
    provide_context=True,
    templates_dict={"model_path": "{{ var.value.project_home }}/model.pth"},
)
```

Explore the [Python SDK](https://neuromation-sdk.readthedocs.io/en/latest/) for more features of the Platform.
