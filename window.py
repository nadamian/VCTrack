import wx
import os
import DataReader
import TrackingObjects
from tracker import Tracker

if __name__ == '__main__':
    app = wx.App()
    window = wx.Frame(None, -1, 'VCTrack')
    window.Show()
    app.MainLoop()
    # data = DataReader.read_data('vocal1DeepCut_resnet50_vocal_strobeMay8shuffle1_200000.h5')
    # t = Tracker(data)
    # t.frame_by()
    # Gonna do this bit with wx now
