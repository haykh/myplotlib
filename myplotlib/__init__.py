import pkg_resources
import matplotlib.pyplot as plt

def loadCustomStyles():
  MPLSTYLE_FILE = pkg_resources.resource_stream(__name__, 'assets/my.mplstyle')
  print (MPLSTYLE_FILE)
  # plt.style.use(MPLSTYLE_FILE)
