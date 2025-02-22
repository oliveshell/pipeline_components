from kfp.components import InputPath, OutputPath, create_component_from_func

def convert_csv_to_apache_parquet(
    data_path: InputPath('CSV'),
    output_data_path: OutputPath('ApacheParquet'),
):
    '''Converts CSV table to Apache Parquet.

    [Apache Parquet](https://parquet.apache.org/)

    Annotations:
        author: Alexey Volkov <alexey.volkov@oliveshell.com>
    '''
    from pyarrow import csv, parquet

    table = csv.read_csv(data_path)
    parquet.write_table(table, output_data_path)


if __name__ == '__main__':
    create_component_from_func(
        convert_csv_to_apache_parquet,
        output_component_file='component.yaml',
        base_image='python:3.7',
        packages_to_install=['pyarrow==0.17.1'],
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/_converters/ApacheParquet/from_CSV/component.yaml",
        },
    )
