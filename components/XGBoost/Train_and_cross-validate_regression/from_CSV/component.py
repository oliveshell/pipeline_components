from collections import OrderedDict
from kfp import components


xgboost_train_regression_and_calculate_metrics_on_csv_op = components.load_component_from_url('https://raw.githubusercontent.com/oliveshell/pipeline_components/2a75b09758df29ff983cdfbacb2f12763cc074f2/components/XGBoost/Train_regression_and_calculate_metrics/from_CSV/component.yaml')
xgboost_5_fold_cross_validation_for_regression_op = components.load_component_from_url('https://raw.githubusercontent.com/oliveshell/pipeline_components/2a75b09758df29ff983cdfbacb2f12763cc074f2/components/XGBoost/Cross_validation_for_regression/from_CSV/component.yaml')


def xgboost_train_and_cv_regression_on_csv(
    data: 'CSV',
    label_column: int = 0,
    objective: str = 'reg:squarederror',
    num_iterations: int = 200,
):
    main_training_and_metrics_task = xgboost_train_regression_and_calculate_metrics_on_csv_op(
        training_data=data,
        testing_data=data,
        label_column=label_column,
        objective=objective,
        num_iterations=num_iterations,
    )

    cv_training_and_metrics_task = xgboost_5_fold_cross_validation_for_regression_op(
        data=data,
        label_column=label_column,
        objective=objective,
        num_iterations=num_iterations,
    )

    return OrderedDict([
        ('model', main_training_and_metrics_task.outputs['model']),

        ('training_mean_absolute_error', main_training_and_metrics_task.outputs['mean_absolute_error']),
        ('training_mean_squared_error', main_training_and_metrics_task.outputs['mean_squared_error']),
        ('training_root_mean_squared_error', main_training_and_metrics_task.outputs['root_mean_squared_error']),
        ('training_metrics', main_training_and_metrics_task.outputs['metrics']),

        ('cv_mean_absolute_error', cv_training_and_metrics_task.outputs['mean_absolute_error']),
        ('cv_mean_squared_error', cv_training_and_metrics_task.outputs['mean_squared_error']),
        ('cv_root_mean_squared_error', cv_training_and_metrics_task.outputs['root_mean_squared_error']),
        ('cv_metrics', cv_training_and_metrics_task.outputs['metrics']),
    ])


if __name__ == '__main__':
    xgboost_train_and_cv_regression_on_csv_op = components.create_graph_component_from_pipeline_func(
        xgboost_train_and_cv_regression_on_csv,
        output_component_file='component.yaml',
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/XGBoost/Train_and_cross-validate_regression/from_CSV/component.yaml",
        },
    )
