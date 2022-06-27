from datetime import timedelta

import pendulum
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import SubprocessFlowRunner
from prefect.orion.schemas.schedules import IntervalSchedule

schedule = IntervalSchedule(
    interval=timedelta(days=1),
    anchor_date=pendulum.datetime(2022, 6, 26, 22, 0, 0, tz="America/Chicago"),
)
DeploymentSpec(
    name="Github-repo-flow",  # name of the deployment
    flow_location="./get_and_process_data.py",  # files contains the flow
    flow_name="get-and-process-data",  # name of the flow
    parameters={"language": "Python"},
    schedule=schedule,  # schedule for the flow
    flow_runner=SubprocessFlowRunner(),  # runner type
    tags=["dev"],
)
