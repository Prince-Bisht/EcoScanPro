"""Train a real MobileNetV2 classifier. Requires tensorflow and labeled images.
Dataset layout: data/waste_images/{Cardboard,Glass,Metal,Organic Waste,Paper,Plastic,General Waste}/image.jpg
The seven class folders must contain licensed, labeled training images.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CLASSES=['Cardboard','Glass','Metal','Organic Waste','Paper','Plastic','General Waste']
def train():
    import tensorflow as tf
    root=ROOT/'data'/'waste_images'
    if not root.exists() or any(not (root/c).exists() for c in CLASSES): raise RuntimeError('Add labeled images in all seven category folders first; see README.')
    train_ds=tf.keras.utils.image_dataset_from_directory(root,validation_split=.2,subset='training',seed=42,image_size=(224,224),batch_size=16,class_names=CLASSES)
    val_ds=tf.keras.utils.image_dataset_from_directory(root,validation_split=.2,subset='validation',seed=42,image_size=(224,224),batch_size=16,class_names=CLASSES)
    base=tf.keras.applications.MobileNetV2(include_top=False,weights='imagenet',input_shape=(224,224,3))
    base.trainable=False
    inp=tf.keras.Input((224,224,3)); x=base(inp,training=False); x=tf.keras.layers.GlobalAveragePooling2D()(x); x=tf.keras.layers.Dropout(.25)(x); out=tf.keras.layers.Dense(len(CLASSES),activation='softmax')(x)
    model=tf.keras.Model(inp,out)
    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    # Training images must use same MobileNetV2 preprocessing as inference.
    def prep(x,y): return tf.keras.applications.mobilenet_v2.preprocess_input(x),y
    train_ds=train_ds.map(prep); val_ds=val_ds.map(prep)
    model.fit(train_ds,validation_data=val_ds,epochs=8,callbacks=[tf.keras.callbacks.EarlyStopping(patience=3,restore_best_weights=True)])
    model.save(ROOT/'models'/'waste_classifier.keras')
    print('Saved model. Evaluate separately on a held-out test set before reporting accuracy.')
if __name__=='__main__': train()
