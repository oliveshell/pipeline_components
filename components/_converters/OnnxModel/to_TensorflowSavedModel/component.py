from kfp.components import create_component_from_func, InputPath, OutputPath


def convert_to_TensorflowSavedModel_from_OnnxModel(
    model_path: InputPath("OnnxModel"),
    converted_model_path: OutputPath("TensorflowSavedModel"),
):
    import onnx
    import onnx_tf

    onnx_model = onnx.load(model_path)
    tf_rep = onnx_tf.backend.prepare(onnx_model)
    tf_rep.export_graph(converted_model_path)


if __name__ == '__main__':
    convert_to_TensorflowSavedModel_from_OnnxModel_op = create_component_from_func(
        convert_to_TensorflowSavedModel_from_OnnxModel,
        output_component_file="component.yaml",
        base_image="tensorflow/tensorflow:2.8.0",
        packages_to_install=["onnx-tf==1.9.0", "onnx==1.11.0"],
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/_converters/OnnxModel/to_TensorflowSavedModel/component.yaml",
        },
    )
