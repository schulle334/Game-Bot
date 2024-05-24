import numpy as np
from skimage.transform import resize

def predict(model, X):
    # Ändern der Bildgröße mit skimage.transform.resize
    X_resized = resize(X, (150, 150, 3), anti_aliasing=True).astype('float32')

    # Normalisieren der Pixelwerte
    X_normalized = X_resized / 255.0

    # Vorhersage mit dem Modell
    Y = model.predict(np.expand_dims(X_normalized, axis=0))

    return Y
