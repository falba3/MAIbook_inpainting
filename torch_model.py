import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms.functional import to_tensor
from PIL import Image
import matplotlib.pyplot as plt


model = fasterrcnn_resnet50_fpn(weights=True)
model.eval()

image = Image.open("images2/castle copy.png")
image_tensor = to_tensor(image).unsqueeze(0)

with torch.no_grad():
    predictions = model(image_tensor)

boxes = predictions[0]["boxes"]
labels = predictions[0]["labels"]
scores = predictions[0]["scores"]

confidence_threshold = 0.5

child_label = 1
child_indices = torch.where((labels == child_label) & (scores > confidence_threshold))
child_boxes = boxes[child_indices]
child_labels = labels[child_indices]
child_scores = scores[child_indices]

plt.imshow(image)
ax = plt.gca()

for box, label, score in zip(child_boxes, child_labels, child_scores):
    x, y, x2, y2 = map(int, box)
    print(box)
    label_name = str(label.item())
    ax.add_patch(plt.Rectangle((x, y), x2 - x, y2 - y, fill=False, color='green', linewidth=2))
    ax.text(x, y - 5, f"Child: {score:.2f}", color='green', fontsize=10, backgroundcolor="white")

plt.axis('off')
plt.show()

