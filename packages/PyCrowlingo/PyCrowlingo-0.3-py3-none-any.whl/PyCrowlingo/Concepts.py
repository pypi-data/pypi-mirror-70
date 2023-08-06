from .Connector import Connector

from .ApiModels import Concepts as Models


class Concepts(Connector):

    def extract(self, text, lang=None, properties=None, precision=None,
                normalizations=None, split=None, model_id=None):
        return Models.Extract.fill(**locals()).call(self.client)

    def train_model(self, model_id, model_version=None):
        return Models.TrainModel.fill(**locals()).call(self.client)

    def create_model(self, model_id, model_version=None):
        return Models.CreateModel.fill(**locals()).call(self.client)

    def deploy_model(self, model_id, model_version=None):
        return Models.DeployModel.fill(**locals()).call(self.client)

    def clear_model(self, model_id, model_version=None):
        return Models.ClearModel.fill(**locals()).call(self.client)

    def create_concept(self, model_id, id=None, properties=None, model_version=None):
        return Models.CreateConcept.fill(**locals()).call(self.client)

    def create_label(self, model_id, text, id=None, concept_id=None, lang=None, precision=None, model_version=None):
        return Models.CreateLabel.fill(**locals()).call(self.client)

    def delete_model(self, model_id, model_version=None):
        return Models.DeleteModel.fill(**locals()).call(self.client)

    def delete_label(self, model_id, label_id, model_version=None):
        return Models.DeleteLabel.fill(**locals()).call(self.client)

    def delete_concept(self, model_id, concept_id, model_version=None):
        return Models.DeleteConcept.fill(**locals()).call(self.client)
