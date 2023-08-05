from ai_transformersx.model import ALL_TASK_MODEL_PATHS, ModelTaskType, ModelMode
from ..transformersx_base import *


@configclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """
    config_name: str = field(None, "Pretrained config name or path if not the same as model_name")

    model_base_dir: str = field("./models/pretrained",
                                "the path base dir of models, model_base_dir and model_name decides the final model path")

    model_name: str = field("bert-base-chinese", "the name of model: " + str(ALL_TASK_MODEL_PATHS))

    model_task_type: str = field("seq_cls",
                                 "the task type of model:{}, model_task_type decides the Task".format(
                                     str(ModelTaskType.names())))

    model_mode: str = field("classification", "the model of model: " + str(ModelMode.names()))

    tokenizer_type: str = field("default", "the name of tokenizer: default,fast")

    language: str = field("cn", "the language of model: cn, en")

    freeze_parameter: str = field("bert", "The parameter name for freeze")

    num_labels: int = field(2, "the number of label")

    def validate(self):
        if not self.model_base_dir:
            raise ValueError("model_base_dir can not be empty.")
