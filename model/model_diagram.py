from sklearn.tree import export_graphviz
import pickle as pkl
import os
from def_model import PKG_DIR

os.chdir(PKG_DIR)

model = pkl.load(open('MODEL', 'rb'))

os.chdir('dot')

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

for i in range(len(model.estimators_)):
    export_graphviz(model.estimators_[i], out_file=f'tree{i + 1}.dot',
        feature_names=['Φ' + str(i + 1).translate(SUB) for i in range(512)] + ['|Z|' + str(i + 1).translate(SUB) for i in range(512)],
        class_names=['Polystyrene', 'Nitrate', 'Sunscreen', 'Plain'],
        rounded=True, filled=True)

for i in range(1, len(model.estimators_) + 1):
    os.system(f'dot -Tpng tree{i}.dot -o ../../model_diagram/tree{i}.png')