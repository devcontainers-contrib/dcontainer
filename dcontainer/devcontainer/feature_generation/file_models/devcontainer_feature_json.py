from easyfs import File

from dcontainer.devcontainer.models.devcontainer_feature import Feature


class DevcontainerFeatureJson(File):
    def __init__(self, feature_model: Feature) -> None:
        super().__init__(feature_model.json(indent=4, exclude_none=True).encode())
