import sys

# PyQt5 kirjastoa tarvitaan esikatseluun (pieni käyttöliittymä):
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

# pypylon on kameran ohjaamisen kirjasto:
from pypylon import pylon

# Numpy ja convolve2d laskentaan
import numpy as np
from scipy.signal import convolve2d

# matplotlib backend kuvien visualisaatioon pyQt5 käyttöliittymässä
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

def init_cam():
    tl_factory = pylon.TlFactory.GetInstance()
    camera = pylon.InstantCamera()
    camera.Attach(tl_factory.CreateFirstDevice())
    camera.Open() # Open connection to the camera
    return camera

def variance_of_laplacian(im):
    laplacian_kernel = np.array(
        [[0,1,0],
        [1,-4,1],
        [0,1,0]])
    kappa_phi = convolve2d(im, laplacian_kernel, mode='same')
    vari = np.var(kappa_phi)
    return kappa_phi, vari

class App(QWidget):

    def __init__(self):
        super().__init__()

        # Luodaan visuaalinen asettelu käyttöliittymälle:
        self.setWindowTitle("Tarkennusdemo")
        hbox = QHBoxLayout()

        # Alustetaan kuvien visualisointi käyttäen Matplotlib backendiä:
        self.figure1 = Figure(figsize=(10,7), tight_layout=True)
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.toolbar_visible = True
        self.figure2 = Figure(figsize=(10,7), tight_layout=True)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.toolbar_visible = True
        hbox.addWidget(self.canvas1)
        hbox.addWidget(self.canvas2)
        self.setLayout(hbox)
        
        # Alustetaan plottaus, eli poistetaan vanha kuvadata muistista
        self.new_plot() 

        # Alustetaan kameraotus käyttöliittymäotukselle:
        
        self.camera = init_cam()
        
        # Asetetaan kameralle ne asetukset, joilla sen halutaan kuvaavan
        self.set_params()
        
        # Käynnistetään kuvaaminen ja kuvan esikatseleminen käyttöliittymässä
        self.start_live()

    def start_live(self):
        """Tämä käynnistää kameran ja visuaalisaation, ei tarvitse tehdä muutoksia"""
        self.camera.StartGrabbing(1)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100) # Milliseconds

    def set_params(self):
        """Selvitä Pylon Viewerin avulla kamerasi ominaisuudet ja kokeile tämän
        aliohjelman sisällä testailla niiden vaikutusta kuvaan. 
        Ennen kuin säädät
        jotain arvoa, opettele tarkastamaan Pylon viewerin avulla, 
        mikä on kyseisen ominaisuuden nimi,
        mitä ovat sen minimi ja maksimiarvot sekä halutun parametrin tyyppi."""
        
        # Kysy kameralta vmin ja vmax arvot pikseleille, jotta ne visualisoituvat nätisti
        self.vmin = self.camera.PixelDynamicRangeMin.GetValue()
        self.vmax = self.camera.PixelDynamicRangeMax.GetValue()

        # Vaihda pikseliformaatti harmaasävyformaatiksi
        self.camera.PixelFormat.SetValue("Mono8")
        

        # Aseta automaattivalotus
        self.camera.ExposureAuto.SetValue("Continuous")
        """
         Tai aseta vakio valotusaika
         self.camera.xxx.xxx(xxx)
        """
        # Kokeile pienentää kameran kuva-alaa (ROI, region of interest)     
        self.camera.Width.SetValue(640)
        self.camera.Height.SetValue(480)

        # Kokeile pienentää kuvan resoluutiota käyttäen binning-toimintoa 
        """(tarkasta ensin Pylon vieweristä tai aiemmin tallentamistasi kameran ominaisuuksita, 
        onko kamerassasi tämä toiminto)"""
        self.camera.BinningHorizontal.SetValue(2)
        self.camera.BinningVertical.SetValue(2)

    def update_frame(self):
        """Päivitä esikatselukuva, älä muuta tätä"""
        # Retrieve a frame as pylon.GrabResult. 2000 is timeout.
        
        grab = self.camera.RetrieveResult(2000, pylon.TimeoutHandling_Return)
        self.image: np.ndarray = grab.GetArray() # Convert to numpy array
        self.display_image(self.image)

    def display_image(self, img: np.ndarray):
        """Koodi, joka laskee fokusta ja visualisoi molemmat kuvat. Ei muutoksia tähän."""
        
        # Putsaa muistista vanha kuva
        self.new_plot()

        # Muunna RGB harmaasävyksi, jos pikseliformaattisi on RGB
        # img = np.array(Image.fromarray(img).convert("L")) # With PIL
        # img = rgb_to_gray(img) # Or using numpy

        # Laske laplacian varianssi tässä kohdin. 
        # Aliohjelma palauttaa im muuttujaan tuloskuvan, lvar muuttujaan varianssilukeman
        im, lvar = variance_of_laplacian(img)

        # Visualisoi kuvat
        self.axes1.imshow(img, cmap="gray", vmin=self.vmin, vmax=self.vmax)
        cmap = self.axes2.imshow(im, cmap="viridis", vmin=0, vmax=20)

        # Piirrä väripalkkiin asteikko (Olemme rajanneet varianssin välille 0 - 20 jotta tulokset visualisoituvat helposti) 
        divider = make_axes_locatable(self.axes2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        self.figure2.colorbar(cmap, cax=cax)

        # Aseta otsikot
        self.axes1.set_title('Kameran näkymä')
        self.axes2.set_title('Analyysitulos: ' + str(np.round(lvar)))

        # Piirrä kuva
        self.canvas1.draw()
        self.canvas2.draw()

        # Do QT stuff - Varmista, että Qt:n sisäisessä käskyrakenteessa ei jää mikään junnaamaan
        app.processEvents()

    def new_plot(self):
        """Siivoaa muistista edellisen kuvan ja luo uuden pohjan seuraavalle kuvalle"""
        self.figure1.clf()
        self.figure2.clf()
        self.axes1 = self.figure1.add_subplot(111, aspect='equal')
        self.axes2 = self.figure2.add_subplot(111, aspect='equal')

if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.app = app
    a.show()
    sys.exit(app.exec_())
