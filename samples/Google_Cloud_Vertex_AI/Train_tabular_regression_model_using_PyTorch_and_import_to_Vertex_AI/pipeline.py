# python3 -m pip install "kfp<2.0.0" "google-cloud-aiplatform>=1.16.0" --upgrade --quiet
from kfp import components

# %% Loading components
download_from_gcs_op = components.load_component_from_url("https://raw.githubusercontent.com/kubeflow/pipelines/c783705c0e566c611ef70160a01e3ed0865051bd/components/contrib/google-cloud/storage/download/component.yaml")
select_columns_using_Pandas_on_CSV_data_op = components.load_component_from_url("https://raw.githubusercontent.com/Ark-kun/pipeline_components/0f0650b8446277b10f7ab48d220e413eef04ec69/components/pandas/Select_columns/in_CSV_format/component.yaml")
fill_all_missing_values_using_Pandas_on_CSV_data_op = components.load_component_from_url("https://raw.githubusercontent.com/Ark-kun/pipeline_components/151411a5b719916b47505cd21c4541c1a5b62400/components/pandas/Fill_all_missing_values/in_CSV_format/component.yaml")
create_fully_connected_pytorch_network_op = components.load_component_from_url("https://raw.githubusercontent.com/Ark-kun/pipeline_components/d8c4cf5e6403bc65bcf8d606e6baf87e2528a3dc/components/PyTorch/Create_fully_connected_network/component.yaml")
train_pytorch_model_from_csv_op = components.load_component_from_url("https://raw.githubusercontent.com/Ark-kun/pipeline_components/d8c4cf5e6403bc65bcf8d606e6baf87e2528a3dc/components/PyTorch/Train_PyTorch_model/from_CSV/component.yaml")
create_pytorch_model_archive_with_base_handler_op = components.load_component_from_url("https://raw.githubusercontent.com/Ark-kun/pipeline_components/46d51383e6554b7f3ab4fd8cf614d8c2b422fb22/components/PyTorch/Create_PyTorch_Model_Archive/with_base_handler/component.yaml")
upload_PyTorch_model_archive_to_Google_Cloud_Vertex_AI_op = components.load_component_from_url("https://raw.githubusercontent.com/Ark-kun/pipeline_components/d1e7a3ccf8f8e0324e15922d6fd90d667fc5281b/components/google-cloud/Vertex_AI/Models/Upload_PyTorch_model_archive/component.yaml")

# %% Pipeline definition
def train_tabular_regression_model_using_PyTorch_pipeline():
    dataset_gcs_uri = "gs://ml-pipeline-dataset/Chicago_taxi_trips/chicago_taxi_trips_2019-01-01_-_2019-02-01_limit=10000.csv"
    feature_columns = ["trip_seconds", "trip_miles", "pickup_community_area", "dropoff_community_area", "fare", "tolls", "extras"]  # Excluded "trip_total"
    label_column = "tips"
    all_columns = [label_column] + feature_columns

    training_data = download_from_gcs_op(
        gcs_path=dataset_gcs_uri
    ).outputs["Data"]

    training_data = select_columns_using_Pandas_on_CSV_data_op(
        table=training_data,
        column_names=all_columns,
    ).outputs["transformed_table"]

    # Cleaning the NaN values.
    training_data = fill_all_missing_values_using_Pandas_on_CSV_data_op(
        table=training_data,
        replacement_value="0",
        #replacement_type_name="float",
    ).outputs["transformed_table"]

    network = create_fully_connected_pytorch_network_op(
        layer_sizes=[len(feature_columns), 10, 1],
        activation_name="elu",
    ).output

    model = train_pytorch_model_from_csv_op(
        model=network,
        training_data=training_data,
        label_column_name=label_column,
        # Optional:
        #loss_function_name="mse_loss",
        #number_of_epochs=1,
        #learning_rate=0.1,
        #optimizer_name="Adadelta",
        #optimizer_parameters={},
        #batch_size=32,
        #batch_log_interval=100,
        #random_seed=0,
    ).outputs["trained_model"]

    model_archive = create_pytorch_model_archive_with_base_handler_op(
        model=model,
        # Optional:
        # model_name="model",
        # model_version="1.0",
    ).outputs["Model archive"]

    vertex_model_name = upload_PyTorch_model_archive_to_Google_Cloud_Vertex_AI_op(
        model_archive=model_archive,
    ).outputs["model_name"]

pipeline_func=train_tabular_regression_model_using_PyTorch_pipeline

# %% Pipeline submission
if __name__ == '__main__':
    from google.cloud import aiplatform
    aiplatform.PipelineJob.from_pipeline_func(pipeline_func=pipeline_func).submit()
