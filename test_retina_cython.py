import timeit
import numpy as np
from os.path import dirname, join
import sys
import cProfile, pstats, io

sys.path.append('C:\\Users\\Nicholas\\Documents\\University @ Glasgow\\Year 5\\cython_test\\retinavision')
import retinavision

sys.path.append('C:\\Users\\Nicholas\\Documents\\University @ Glasgow\\Year 5\\cython_test\\retinavision_cython\\memory view')
from memoryView import sum3d

sys.path.append('C:\\Users\\Nicholas\\Documents\\University @ Glasgow\\Year 5\\cython_test\\retinavision_cython\\retina')
import retina_sample
import retina_utils


datadir = join(dirname(dirname(__file__)), "cython_test")

# generate a random 2 dimensional array
input_img =  np.random.randint(256, size=(720, 1280), dtype=np.uint8)
padding = 1
fixation = (640.0, 360.0)
campicShape = (720, 1280, 3)
arr = np.zeros((40, 40, 40), dtype=int)

def runOriginalPad():
    return retinavision.utils.pad(input_img, padding, True)

def runCythonPad():
    image = input_img.astype(np.float64)
    return retina_utils.pad(image, padding, True)

def runCPadMemView():
    return padMemoryView(input_img, padding, False)

def originalRetinaSample():
    R = retinavision.Retina()
    R.loadLoc(join(datadir, "retinavision_cython", "data", "retinas", "ret50k_loc.pkl"))
    R.loadCoeff(join(datadir, "retinavision_cython", "data", "retinas", "ret50k_coeff.pkl"))
    R.prepare(campicShape, fixation)
    v = R.sample(input_img, fixation)
    return v

def cythonRetinaSample():
    R = retina_sample.Retina()
    retina_sample.loadCoeff()
    retina_sample.loadLoc()
    R.updateLoc()
    image = input_img.astype(np.float64)
    v = R.sample(image, fixation)
    return v

def testCython():
    py = timeit.timeit('''runOriginal()''',setup="from __main__ import runOriginal",number=100)
    cy = timeit.timeit('''runCPad()''',setup="from __main__ import runCPad", number=100)

    print(cy, py)
    print('Cython is {}x faster'.format(py/cy))

def testMemoryView():
    py = timeit.timeit('''runCPad()''',setup="from __main__ import runCPad",number=100)
    cy = timeit.timeit('''runCPadMemView()''',setup="from __main__ import runCPadMemView", number=100)

    print(cy, py)
    print('Memory View is {}x faster'.format(py/cy))

def testMemoryExampleCode():
    py = timeit.timeit('''old_sum3d(arr)''',setup="from __main__ import old_sum3d",number=100)
    cy = timeit.timeit('''sum3d(arr)''',setup="from __main__ import sum3d", number=100)

    print(cy, py)
    print('Memory View is {}x faster'.format(py/cy))

def testRetinaSample():
    py = timeit.timeit('''old_sum3d()''',setup="from __main__ import old_sum3d",number=100)
    cy = timeit.timeit('''sum3d()''',setup="from __main__ import sum3d", number=100)

    print(cy, py)
    print('Memory View is {}x faster'.format(py/cy))

def testLoadPickle():
    coeff = loadpickle.loadCoeff(join(datadir, "retinas", "ret50k_coeff.pkl"))
    return coeff[0][2]

def compareRetinaSample():
    py = timeit.timeit('''originalRetinaSample()''',setup="from __main__ import originalRetinaSample",number=10)
    cy = timeit.timeit('''cythonRetinaSample()''',setup="from __main__ import cythonRetinaSample", number=10)

    print(cy, py)
    print('Cython is {}x faster'.format(py/cy))

def compareRetinaPad():
    py = timeit.timeit('''runOriginalPad()''',setup="from __main__ import runOriginalPad",number=10)
    cy = timeit.timeit('''runCythonPad()''',setup="from __main__ import runCythonPad", number=10)

    print(cy, py)
    print('Cython is {}x faster'.format(py/cy))

def cythonRetinaProfile():
    R = retina_sample.Retina()
    retina_sample.loadCoeff()
    retina_sample.loadLoc()
    R.updateLoc()
    image = input_img.astype(np.float64)
    cProfile.runctx("R.sample(image, fixation)", globals(), locals(), "Profile.prof")
    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("cumtime").print_stats()

def testOutput():
    original = originalRetinaSample()
    cythonised = cythonRetinaSample()

    print(original)
    print(cythonised)
    for index, (first, second) in enumerate(zip(original, cythonised)):
        if first != second:
            print(index, first, second)

# originalRetinaSample()
# print("------------------------------------")
# cythonRetinaSample()

compareRetinaSample()
# # originalRetinaSample()
# cythonRetinaProfile()
# testOutput()

# nan_array = np.array([[0, np.nan, 1.0], [np.nan, 3434, 1.0], [343, np.nan, 1.0], [np.nan, np.nan, 1.0], [np.nan, np.nan, 1.0], [np.nan, 345345, 1.0]])

# m = retina_sample.mask_where_isnan(nan_array)

# print(m)
