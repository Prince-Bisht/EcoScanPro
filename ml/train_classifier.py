"""Train MobileNetV2 on the six available TrashNet categories."""
from logging import root
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CLASSES = [
    "Cardboard",
    "E-Waste",
    "General Waste",
    "Glass",
    "Metal",
    "Organic Waste",
    "Paper",
    "Plastic"
]


def train():
    import tensorflow as tf

    extensions = {".jpg", ".jpeg", ".png", ".webp"}
    root = ROOT / "data" / "waste_images"

    counts = {
    name: sum(
        1 for file in (root / name).rglob("*")
        if file.is_file() and file.suffix.lower() in extensions
    )
    for name in CLASSES
}
    if any(count == 0 for count in counts.values()):
        raise RuntimeError(f'Missing training images: {counts}')

    unexpected = [p.name for p in root.iterdir() if p.is_dir() and p.name not in CLASSES]
    if unexpected:
        raise RuntimeError(f'Remove or move extra category folders before training: {unexpected}')

    common = dict(validation_split=0.2, seed=42, image_size=(224, 224),
                  batch_size=16, class_names=CLASSES)
    train_ds = tf.keras.utils.image_dataset_from_directory(root, subset='training', **common)
    val_ds = tf.keras.utils.image_dataset_from_directory(root, subset='validation', **common)
    preprocess = tf.keras.applications.mobilenet_v2.preprocess_input
    train_ds = train_ds.map(lambda x, y: (preprocess(x), y)).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (preprocess(x), y)).prefetch(tf.data.AUTOTUNE)

    base = tf.keras.applications.MobileNetV2(
        include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    base.trainable = False
    inp = tf.keras.Input(shape=(224, 224, 3))
    x = base(inp, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    out = tf.keras.layers.Dense(len(CLASSES), activation='softmax')(x)
    model = tf.keras.Model(inp, out)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_ds, validation_data=val_ds, epochs=8,
              callbacks=[tf.keras.callbacks.EarlyStopping(
                  monitor='val_loss', patience=3, restore_best_weights=True)])

    output = ROOT / 'models'
    output.mkdir(parents=True, exist_ok=True)
    model.save(output / 'waste_classifier.keras')
    (output / 'waste_classifier_classes.json').write_text(json.dumps(CLASSES, indent=2))
    print('Model and class mapping saved. Evaluate on a separate held-out test set.')


if __name__ == '__main__':
    train()
