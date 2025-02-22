from kfp.components import create_component_from_func


def get_size_of_list(
    list: list,
) -> int:
    """Gets size of a JSON array."""
    return len(list)


if __name__ == "__main__":
    get_size_of_list_op = create_component_from_func(
        get_size_of_list,
        base_image="python:3.10",
        output_component_file="component.yaml",
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/json/List/Get_size/component.yaml",
        },
    )
