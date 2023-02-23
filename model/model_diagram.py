from sklearn.tree import export_graphviz
import pickle as pkl
import os
from dir_model import PKG_DIR

os.chdir(PKG_DIR)

model = pkl.load(open('MODEL_MAT_UPDATED', 'rb'))

os.chdir('dot')

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

for j in range(len(model.estimators_)):
    export_graphviz(model.estimators_[j], out_file=f'tree{j + 1}.dot',
        feature_names=['Φ' + str((i + 1) // 2).translate(SUB) if (i + 1) % 2 == 0 else '|Z|' + str(((i + 1) // 2) + 1).translate(SUB) for i in range(1024)],
        class_names=['Polystyrene', 'Nitrate', 'Sunscreen'],
        rounded=True, filled=True)

for i in range(1, len(model.estimators_) + 1):
    os.system(f'dot -Tpng tree{i}.dot -o ../../model_diagram/tree{i}.png')

for i in range(1, len(model.estimators_) + 1):
    os.system(f'rm tree{i}.dot')