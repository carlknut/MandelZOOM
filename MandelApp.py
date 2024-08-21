import wx
import numpy as np
import MandelZoom as MZ
import time

W = 750#960
H = 300#540

filename = 'C:\\Users\\thorr\\OneDrive\\Desktop\\MandelZoom\\MZF9_Frames\\mandelbrot_'

def isNumber(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def inRange(real,imag):
    if real >= -2 and real <= 0.5 and imag >= -1.25 and imag <= 1.25:
        return True
    else:
        return False


class Mwin(wx.Frame):
    def __init__(self, parent, title, size):
        super(Mwin, self).__init__(parent, title=title, size = (W,H))

        self.zp = (0,0)
        self.zf = 0
        self.dim = (1920,1080)
        self.initIters = 100
        self.maxIters = 750
        self.totalFrames = 300
        self.startingFrame = 0
        self.colourRange = np.array([155,180])

        # Font Styles
        self.font1 = wx.Font(20, family = wx.FONTFAMILY_ROMAN, style = 0, weight = 90, 
                underline = True, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        self.font2 = wx.Font(15, family = wx.FONTFAMILY_ROMAN, style = 0, weight = 90, 
                underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        self.font3 = wx.Font(10, family = wx.FONTFAMILY_ROMAN, style = wx.ITALIC, weight = 90, 
                underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)

        # Panel and Main Box for Gui
        panel = wx.Panel(self)
        mainbox = wx.BoxSizer(wx.HORIZONTAL)

        # Box for Zoom Point Settings
        vbox1 = wx.BoxSizer(wx.VERTICAL)

        # Zoom Point Title
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        zpL = wx.StaticText(panel, -1, "Zoom Point:")
        zpL.SetFont(self.font1)
        hbox1.Add(zpL,0,wx.ALIGN_LEFT,5)
        vbox1.Add(hbox1)

        # Real Part of Zoom Point
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        rL = wx.StaticText(panel, -1, "Real:")
        rL.SetFont(self.font2)
        self.rT = wx.TextCtrl(panel)
        self.rT.SetLabel(str(self.zp[0]))
        hbox2.AddStretchSpacer(20)
        hbox2.Add(rL,0,wx.ALIGN_LEFT,5)
        hbox2.Add(self.rT,0,wx.ALIGN_LEFT,5)
        vbox1.Add(hbox2)

        # Imaginary Part of Zoom Point
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        iL = wx.StaticText(panel, -1, "Imag:")
        iL.SetFont(self.font2)
        self.iT = wx.TextCtrl(panel)
        self.iT.SetLabel(str(self.zp[1]))        
        hbox3.Add(iL,0,wx.ALIGN_LEFT,5)
        hbox3.Add(self.iT,0,wx.ALIGN_LEFT,5)
        vbox1.Add(hbox3)

        # Zoom Point Error or Confirmation Messege 
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.messege = wx.StaticText(panel, -1, "ERROR")
        self.messege.SetFont(self.font3)
        self.messege.SetForegroundColour(wx.Colour(255,0,0))
        hbox4.Add(self.messege,0,wx.ALIGN_LEFT,5)
        vbox1.Add(hbox4)

        # Zoom Point Confirmation Button
        self.zpB = wx.Button(panel, label = "Confirm Point")
        self.zpB.Bind(wx.EVT_BUTTON, self.zpConfirm)
        vbox1.Add(self.zpB,0,wx.ALIGN_CENTER_HORIZONTAL,5)

        # Zoom Factor Title
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        zfL = wx.StaticText(panel, -1, label = "Zoom Factor:")
        zfL.SetFont(self.font1)
        hbox5.Add(zfL,0,wx.ALIGN_LEFT,5)
        vbox1.Add(hbox5)

        # Zoom Factor Text Field
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.zfT = wx.TextCtrl(panel)
        self.zfT.SetLabel(str(self.zf))
        hbox6.Add(self.zfT)
        vbox1.Add(hbox6)

        # Zoom Factor Error or Confirmation Messege
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.messege2 = wx.StaticText(panel,-1, "ERROR")
        self.messege2.SetFont(self.font3)
        self.messege2.SetForegroundColour(wx.Colour(255,0,0))
        hbox7.Add(self.messege2,0,wx.ALIGN_LEFT,5)
        vbox1.Add(hbox7)

        # Zoom Factor Confirmation Button
        self.zfB = wx.Button(panel, label = "Confirm Factor")
        self.zfB.Bind(wx.EVT_BUTTON, self.zfConfirm)
        vbox1.Add(self.zfB,0,wx.ALIGN_CENTER_HORIZONTAL,5)        



        # Box for Render Options
        ovbox = wx.BoxSizer(wx.VERTICAL)
        
        # Render Options Title
        roLbox = wx.BoxSizer(wx.HORIZONTAL)
        roL = wx.StaticText(panel, -1, label = "Rendering Options")
        roL.SetFont(self.font1)
        roLbox.Add(roL,0,wx.ALIGN_CENTER_VERTICAL,5)
        ovbox.Add(roLbox)

        # Rendering Options Configuration box
        ohbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Options Label Box
        labelBox = wx.BoxSizer(wx.VERTICAL)
        labelList = ["Dimensions:","Initial Iters:","Max Iters:","Total Frames:","Starting Frame:"]
        for l in labelList:
            #tempBox = wx.BoxSizer(wx.HORIZONTAL)
            tempLabel = wx.StaticText(panel,-1,label = str(l))
            tempLabel.SetFont(self.font2)
            labelBox.Add(tempLabel,0,wx.ALIGN_LEFT,5)
        ohbox1.Add(labelBox)
        
        # Options Entry Field Box
        entryBox = wx.BoxSizer(wx.VERTICAL)

        dimBox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.dimW = wx.TextCtrl(panel,-1,size=(55,20),value=str(self.dim[0]))
        dimBox.Add(self.dimW,0,wx.ALIGN_LEFT,5)

        self.dimH = wx.TextCtrl(panel,-1,size=(55,20),value=str(self.dim[1]))
        dimBox.Add(self.dimH,0,wx.ALIGN_LEFT,5)

        entryBox.Add(dimBox)
        
        self.iitersT = wx.TextCtrl(panel,-1,value=str(self.initIters))
        entryBox.Add(self.iitersT,0,wx.ALIGN_LEFT,5)

        self.mitersT = wx.TextCtrl(panel,-1,value=str(self.maxIters))
        entryBox.Add(self.mitersT,0,wx.ALIGN_LEFT,5)

        self.tfT = wx.TextCtrl(panel,-1,value=str(self.totalFrames))
        entryBox.Add(self.tfT,0,wx.ALIGN_LEFT,5)

        self.sfT = wx.TextCtrl(panel,-1,value=str(self.startingFrame))
        entryBox.Add(self.sfT,0,wx.ALIGN_LEFT,5)

        ohbox1.Add(entryBox)

        # Options Error Box
        errorBox = wx.BoxSizer(wx.VERTICAL)

        ovbox.Add(ohbox1)
        
        # Option Confirm Messege
        self.omessege = wx.StaticText(panel,-1,label="")
        self.omessege.SetFont(self.font3)
        ovbox.Add(self.omessege,0,wx.ALIGN_LEFT,5)
        
        # Options Confirm Button
        oB = wx.Button(panel,-1, label = "Confirm Options")
        oB.Bind(wx.EVT_BUTTON, self.confirmOptions)        
        ovbox.Add(oB,0,wx.ALIGN_CENTRE_HORIZONTAL,5)

    
        # Colour Selection box
        cvbox = wx.BoxSizer(wx.VERTICAL)

        # Colour Label
        cLhbox = wx.BoxSizer(wx.HORIZONTAL)
        cL = wx.StaticText(panel,-1, label = "Colour Selection:")
        cL.SetFont(self.font1)
        cLhbox.Add(cL,0,wx.ALIGN_LEFT,5)
        cvbox.Add(cLhbox)
        
        # Colour Slider
        cshbox1 = wx.BoxSizer(wx.HORIZONTAL)
        csL1 = wx.StaticText(panel,-1,label = "Start: ")
        csL1.SetFont(self.font2)
        self.colourSlider1 = wx.Slider(panel,-1,value=0,minValue=0,maxValue=255,size=(200,20))
        self.colourSlider1.Bind(wx.EVT_SLIDER,self.colourSelect)
        cshbox1.Add(csL1,0,wx.ALIGN_LEFT,5)
        cshbox1.Add(self.colourSlider1,0,wx.ALIGN_LEFT,5)
        
        cshbox2 = wx.BoxSizer(wx.HORIZONTAL)
        csL2 = wx.StaticText(panel,-1,label= "            ") # 12 Spaces
        csL2.SetFont(self.font2)
        csimg_file = 'C:\\Users\\thorr\\OneDrive\\Desktop\\MandelZoom\\GUI Images\\hue_slider.bmp'
        csimg = wx.Image(csimg_file,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        csbmp = wx.StaticBitmap(panel,-1,csimg)
        cshbox2.Add(csL2)
        cshbox2.Add(csbmp)

        cshbox3 = wx.BoxSizer(wx.HORIZONTAL)
        csL3 = wx.StaticText(panel,-1,label = "End:  ")
        csL3.SetFont(self.font2)
        self.colourSlider2 = wx.Slider(panel,-1,value=255,minValue=0,maxValue=255,size=(200,20))
        self.colourSlider2.Bind(wx.EVT_SLIDER,self.colourSelect)
        cshbox3.Add(csL3,0,wx.ALIGN_LEFT,5)
        cshbox3.Add(self.colourSlider2,0,wx.ALIGN_LEFT,5)

        cshbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hrL = wx.StaticText(panel,-1,label= "Hue Range:  ")
        hrL.SetFont(self.font2)
        self.shT = wx.TextCtrl(panel,-1,value=str(self.colourSlider1.GetValue()),size=(40,20),style=wx.TE_PROCESS_ENTER)
        self.shT.Bind(wx.EVT_TEXT_ENTER,self.colourText)
        to = wx.StaticText(panel,-1,label=" to ")
        self.ehT = wx.TextCtrl(panel,-1,value=str(self.colourSlider2.GetValue()),size=(40,20))

        cshbox4.Add(hrL)
        cshbox4.Add(self.shT)
        cshbox4.Add(to)
        cshbox4.Add(self.ehT)

        cmessegehbox = wx.BoxSizer(wx.HORIZONTAL)
        self.cmessege = wx.StaticText(panel,-1, label="")
        self.cmessege.SetFont(self.font3)
        cmessegehbox.Add(self.cmessege)
        
        
        ccB = wx.Button(panel,-1,label= "Confirm Colour")
        ccB.Bind(wx.EVT_BUTTON,self.confirmColour)
        
        cvbox.Add(cshbox1)
        cvbox.Add(cshbox2)
        cvbox.Add(cshbox3)
        cvbox.Add(cshbox4)
        cvbox.Add(cmessegehbox)
        cvbox.Add(ccB,0,wx.ALIGN_CENTER_HORIZONTAL,5)
        

        # Rendering Buttons box
        rbbox = wx.BoxSizer(wx.VERTICAL)
        
        # Test Render Button
        self.trB = wx.Button(panel, label = "Test Render")
        self.trB.Bind(wx.EVT_BUTTON,self.testRender)
        rbbox.Add(self.trB,0,wx.ALIGN_CENTER_HORIZONTAL,5)

        # Full Render Button
        self.frB = wx.Button(panel, label = "Full Render")
        self.frB.Bind(wx.EVT_BUTTON,self.fullRender)
        rbbox.Add(self.frB,0,wx.ALIGN_CENTER_HORIZONTAL,5)


        
        mainbox.Add(vbox1)
        mainbox.Add(ovbox)
        mainbox.Add(cvbox)
        mainbox.Add(rbbox)
        panel.SetSizer(mainbox)
        
        self.Centre()
        self.Show()

    # Method to Set Zoom Point Text
    def setZPText(self):
        self.rT.SetLabel(str(self.zp[0]))
        self.iT.SetLabel(str(self.zp[1]))

    # Event for Zoom Point Button
    def zpConfirm(self, event):
        self.messege.SetLabel("")
        real = self.rT.GetValue()
        imag = self.iT.GetValue()
        if isNumber(real) and isNumber(imag):
            real = float(real)
            imag = float(imag)
            if inRange(real,imag):
                self.messege.SetForegroundColour(wx.Colour(0,0,255))
                self.messege.SetLabel("Zoom Point Set")
                self.zp = (real,imag)
                self.setZPText()
                print(self.zp)
            else:
                self.messege.SetForegroundColour(wx.Colour(255,0,0))
                self.messege.SetLabel("Value out of Range")
                self.setZPText()
        else:
            self.messege.SetForegroundColour(wx.Colour(255,0,0))
            self.messege.SetLabel("Entry must be a number")
            self.setZPText()

    # Event for Zoom Factor Button
    def zfConfirm(self, event):
        self.messege2.SetLabel("")
        factor = self.zfT.GetValue()
        if isNumber(factor):
            factor = float(factor)
            if factor >= 1:
                self.messege2.SetForegroundColour(wx.Colour(0,0,255))
                self.messege2.SetLabel("Zoom Factor Set")
                self.zf = factor
            else:
                self.messege2.SetForegroundColour(wx.Colour(255,0,0))
                self.messege2.SetLabel("Must be greater than 1")
                self.zfT.SetLabel(str(self.zf))
        else:
            self.messege2.SetForegroundColour(wx.Colour(255,0,0))
            self.messege2.SetLabel("Entry must be a number")
            self.zfT.SetLabel(str(self.zf))

    # Event for Confirm Options Button
    def confirmOptions(self, event):
        self.dim = (int(self.dimW.GetValue()),int(self.dimH.GetValue()))
        self.initIters = int(self.iitersT.GetValue())
        self.maxIters = int(self.mitersT.GetValue())
        self.totalFrames = int(self.tfT.GetValue())
        self.startingFrame = int(self.sfT.GetValue())

        self.omessege.SetForegroundColour(wx.Colour(0,0,255))
        self.omessege.SetLabel("Options Confirmed")

    # Event for Colour Sliders
    def colourSelect(self, event):
        self.shT.SetLabel( str(self.colourSlider1.GetValue()) )
        self.ehT.SetLabel( str(self.colourSlider2.GetValue()) )

        self.cmessege.SetLabel("")

    # Event for Manually Entering Values
    def colourText(self, event):
        self.colourSlider1.SetValue( int(self.shT.GetLabel()) )

    # Event for Confirm Colour Button
    def confirmColour(self, event):
        self.colourRange[0] = int(self.colourSlider1.GetValue())
        self.colourRange[1] = int(self.colourSlider2.GetValue())
        self.cmessege.SetForegroundColour(wx.Colour(0,0,255))
        self.cmessege.SetLabel("Colour Confirmed")
        

    # Event for Test Render Button
    def testRender(self, event):

        fname = 'C:\\Users\\thorr\\OneDrive\\Desktop\\MandelZoom\\test_frames\\mandelbrot_'
        start_time = time.time()
        print(start_time)
        MZ.mandelanim(complex(self.zp[0],self.zp[1]),float(1/self.zf),(480,270),self.initIters,self.maxIters,self.totalFrames,self.startingFrame,fname,self.colourRange)
        duration = time.time() - start_time
        print("Total duration: " + str(duration) + " s")

    # Event for Full Render Button
    def fullRender(self, event):
        start_time = time.time()
        print("Start Time: "+ str(start_time))
        MZ.mandelanim(complex(self.zp[0],self.zp[1]),float(1/self.zf),(self.dim[0],self.dim[1]),self.initIters,self.maxIters,self.totalFrames,self.startingFrame,filename,self.colourRange)
        duration = time.time() - start_time
        print("Total duration: " + str(duration) + " s")


    
def main():
    app = wx.App() 
    Mwin(None, title = "MandelZOOM", size = (W,H)) 
    app.MainLoop()

if __name__ == '__main__':
    main()
