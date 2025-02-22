from typing import NamedTuple

from kfp.components import create_component_from_func

def create_study_in_gcp_ai_platform_optimizer(
    study_id: str,
    parameter_specs: list,
    optimization_goal: str = 'MAXIMIZE',
    metric_specs: list = None,
    gcp_project_id: str = None,
    gcp_region: str = "us-central1",
) -> NamedTuple('Outputs', [
    ("study_name", str),
]):
    """Creates a Google Cloud AI Plaform Optimizer study.
    See https://cloud.google.com/ai-platform/optimizer/docs

    Annotations:
        author: Alexey Volkov <alexey.volkov@oliveshell.com>

    Args:
        study_id: Name of the study.
        parameter_specs: List of parameter specs. See https://cloud.google.com/ai-platform/optimizer/docs/reference/rest/v1/projects.locations.studies#parameterspec
        optimization_goal: Optimization goal when optimizing a single metric. Can be MAXIMIZE (default) or MINIMIZE. Ignored if metric_specs list is provided.
        metric_specs: List of metric specs. See https://cloud.google.com/ai-platform/optimizer/docs/reference/rest/v1/projects.locations.studies#metricspec
    """

    import logging
    import google.auth

    logging.getLogger().setLevel(logging.INFO)

    # Validating and inferring the arguments
    if not gcp_project_id:
        _, gcp_project_id = google.auth.default()

    # Building the API client.
    # The main API does not work, so we need to build from the published discovery document.
    def create_caip_optimizer_client(project_id):
        from googleapiclient import discovery
        # The discovery is broken. See https://github.com/googleapis/google-api-python-client/issues/1470
        # return discovery.build("ml", "v1")
        return discovery.build("ml", "v1", discoveryServiceUrl='https://storage.googleapis.com/caip-optimizer-public/api/ml_public_google_rest_v1.json')

    ml_api = create_caip_optimizer_client(gcp_project_id)

    if not metric_specs:
        metric_specs=[{
            'metric': 'metric',
            'goal': optimization_goal,
        }]
    study_config = {
        'algorithm': 'ALGORITHM_UNSPECIFIED',  # Let the service choose the `default` algorithm.
        'parameters': parameter_specs,
        'metrics': metric_specs,
    }
    study = {'study_config': study_config}

    create_study_request = ml_api.projects().locations().studies().create(
        parent=f'projects/{gcp_project_id}/locations/{gcp_region}',
        studyId=study_id,
        body=study,
    )
    create_study_response = create_study_request.execute()
    study_name = create_study_response['name']
    return (study_name,)


if __name__ == '__main__':
    create_study_in_gcp_ai_platform_optimizer_op = create_component_from_func(
        create_study_in_gcp_ai_platform_optimizer,
        base_image='python:3.8',
        packages_to_install=['google-api-python-client==1.12.3', 'google-auth==1.21.3'],
        output_component_file='component.yaml',
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/google-cloud/Optimizer/Create_study/component.yaml",
        },
    )
