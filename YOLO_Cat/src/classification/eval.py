import torch
from torchvision.datasets import ImageFolder
from torchvision.transforms import transforms
from Classifier import get_pretrained_model
import tqdm
model, _ = get_pretrained_model('convnextv2-n')

transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = ImageFolder('/media/yhy/YHYSSD1T/Dataset/ILSVRC2012/images/val', transform=transforms)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=256, shuffle=False, num_workers=8)

model.eval()
correct = 0

for images, labels in tqdm.tqdm(dataloader):
    images = images.cuda()
    with torch.no_grad():
        outputs = model(images).logits
        _, predicted = torch.max(outputs, 1)
        correct += (predicted == labels.cuda()).sum().item()
        
print(f"Accuracy: {correct / len(dataset)}")