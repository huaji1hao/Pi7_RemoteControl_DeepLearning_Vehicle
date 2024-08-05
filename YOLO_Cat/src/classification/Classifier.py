from transformers import ConvNextV2ForImageClassification, ConvNextV2Model, ConvNextV2Config, AutoProcessor

map_dict = {
    'convnextv2-n': 'model_weights/convnext/v2-n'
}
def get_pretrained_model(name, **kwargs):
    if name in map_dict:
        processor = AutoProcessor.from_pretrained(map_dict[name])
        model = ConvNextV2ForImageClassification.from_pretrained(map_dict[name]).cuda()
        # model_backbone = model.convnextv2
        return model, processor
    else:
        raise ValueError(f"model {name} not found")