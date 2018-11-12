import holoclean

from detect import NullDetector, ViolationDetector
from repair.featurize import InitFeaturizer
from repair.featurize import InitAttFeaturizer
from repair.featurize import InitSimFeaturizer
from repair.featurize import FreqFeaturizer
from repair.featurize import OccurFeaturizer
from repair.featurize import ConstraintFeat
from repair.featurize import LangModelFeat


# 1. Setup a HoloClean session.
hc = holoclean.HoloClean(pruning_topk=0.1, epochs=30, weight_decay=0.01, threads=20, batch_size=1, verbose=True, timeout=3*60000).session

# 2. Load training data and denial constraints.
hc.load_data('adult', '/datasets/holoclean/ProfilerDatasets', 'adult_1.csv')
hc.load_dcs('/datasets/holoclean/ProfilerDatasets', 'adult_constraints.txt')
hc.ds.set_constraints(hc.get_dcs())

# 3. Detect erroneous cells using these two detectors.
detectors = [NullDetector(), ViolationDetector()]
hc.detect_errors(detectors)

# 4. Repair errors utilizing the defined features.
hc.setup_domain()
featurizers = [InitAttFeaturizer(), InitSimFeaturizer(), FreqFeaturizer(), OccurFeaturizer(), LangModelFeat(), ConstraintFeat()]
hc.repair_errors(featurizers)

# 5. Evaluate the correctness of the results.
def get_tid(row):
    return row['tid'] - 1

def get_attr(row):
    return row['attribute'].lower()

def get_value(row):
    return row['correct_val'].lower()

# hc.evaluate('data', 'hospital_clean.csv', get_tid, get_attr, get_value)
