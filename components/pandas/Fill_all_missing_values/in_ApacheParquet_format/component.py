from kfp.components import InputPath, OutputPath, create_component_from_func


def fill_all_missing_values_using_Pandas_on_ApacheParquet_data(
    table_path: InputPath("ApacheParquet"),
    transformed_table_path: OutputPath("ApacheParquet"),
    replacement_value: str = "0",
    column_names: list = None,
):
    import pandas

    df = pandas.read_parquet(path=table_path)
    for column_name in column_names or df.columns:
        column = df[column_name]
        # The `.astype` method does not work correctly on booleans
        # So we need to special-case them
        if pandas.api.types.is_bool_dtype(column.dtype):
            if replacement_value.lower() in ("true", "1"):
                converted_replacement_value = True
            elif replacement_value.lower() in ("false", "0"):
                converted_replacement_value = False
            else:
                raise ValueError(
                    f"Cannot convert value '{replacement_value}' to boolean for column {column_name}."
                )
        else:
            # Using Pandas to convert the replacement_value to column.dtype.
            converted_replacement_value = pandas.Series(
                replacement_value, dtype=column.dtype
            ).tolist()[0]

        print(
            f"Filling missing values in column '{column_name}' with '{converted_replacement_value}'"
        )
        column.fillna(value=converted_replacement_value)

    df.to_parquet(
        path=transformed_table_path,
        index=False,
    )


if __name__ == "__main__":
    fill_all_missing_values_using_Pandas_on_ApacheParquet_data_op = create_component_from_func(
        fill_all_missing_values_using_Pandas_on_ApacheParquet_data,
        output_component_file="component.yaml",
        base_image="python:3.9",
        packages_to_install=[
            "pandas==1.4.1",
            "pyarrow==9.0.0",
        ],
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/pandas/Fill_all_missing_values/in_ApacheParquet_format/component.yaml",
        },
    )
