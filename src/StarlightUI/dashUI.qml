import QtQuick 2.0
import QtQuick.Window 2.0
import QtGraphicalEffects 1.14
import QtQuick.Controls 1.1

ApplicationWindow {
    width: 1024
    height: 600
    visible: true
    color: colorVal
    title: qsTr("Car Stuff")
    property string rdsText: "Plc"
    property string radioBand: "Band"
    property string freq: "00.0"
    property string stationMem: ""
    property string modType: "MHz"
    property string source: "Source"
    property string volume: "0"
    property string time: "00:00"
    property string date: "01/01/1970"
    property bool isVolumeChanging: false
    property string colorVal: "#750273"
    property bool showAudioMenu: false
    property bool isBass: false
    property bool isTreble: false
    property bool isLoudness: false
    property bool isAutoVol: false
    property bool isRFBal: false
    property bool isLRBal: false
    property bool isEQPreset: false
    property string loudValue: "0"
    property string autoVolValue: "0"
    property string bassValue: "0"
    property string trebleValue: "0"
    property string lrValue: "0"
    property string rfValue: "0"
    property string eqPresetValue: "None"
    property string srcImage: "radio.png"
    property bool showMainMenu: false
    property bool isListVisible: false
    property var trackList: [" ","Loading..."," "," "]
    property var trackListSel: [false, false, false, false]
    property var tripInfo: ["--","--.-","--"]
    property bool darkMode: false
    property var tripImage: ["trip_gasstation.png", "trip_fuel.png", "trip_distance.png"]



    //flags: Qt.FramelessWindowHint | Qt.Window


    Rectangle {
        id: rectangleBack
        x: 10
        y: 9
        width: 1004
        height: 583
        color: "#68ffffff"
        radius: 12
        visible: true

        DropShadow {
            opacity: 0.5
            anchors.fill: headUnitBox
            horizontalOffset: 3
            verticalOffset: 3
            radius: 8.0
            samples: 17
            color: "#80000000"
            source: headUnitBox
        }


        DropShadow {
            opacity: 0.5
            anchors.fill: tripBox
            horizontalOffset: 3
            verticalOffset: 3
            radius: 8.0
            samples: 17
            color: "#80000000"
            source: tripBox
        }

        Rectangle {
            id: headUnitBox
            x: 134
            y: 98
            width: 737
            height: 185
            color: "#60ffffff"
            radius: 15
            border.width: 0


            Text {
                id: sourceText
                x: 8
                y: 8
                width: 721
                height: 26
                text: source
                font.pixelSize: 19
                horizontalAlignment: Text.AlignHCenter
                textFormat: Text.RichText
                minimumPixelSize: 12
            }

            Image {
                id: stationImage
                x: 319
                y: 67
                width: 52
                height: 52
                source: "img/" + srcImage
                fillMode: Image.PreserveAspectFit
            }

            Text {
                id: rdsTxt
                x: 388
                y: 40
                width: 225
                height: 35
                text: rdsText
                font.pixelSize: 30
                horizontalAlignment: (source == "Radio" || rdsTxt == "Radio Off") ? Text.AlignHCenter : Text.AlignLeft
                textFormat: Text.RichText
                elide: Text.ElideRight
            }

            Text {
                id: freqText
                x: 388
                y: 77
                width: 331
                height: 32
                text: freq + " " + modType
                font.pixelSize: 28
                textFormat: Text.RichText
            }

            Text {
                id: bandTxt
                x: 388
                y: 116
                width: 159
                height: 31
                text: radioBand
                font.pixelSize: 24
                textFormat: Text.RichText
                elide: Text.ElideRight
            }

            Text {
                id: memTxt
                x: 515
                y: 119
                text: stationMem
                font.pixelSize: 20
                textFormat: Text.RichText
            }

            Text {
                id: dateTxt
                x: 53
                y: 102
                width: 204
                height: 29
                text: date
                font.pixelSize: 24
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
                textFormat: Text.RichText
            }

            Text {
                id: timeTxt
                x: 53
                y: 53
                width: 204
                height: 43
                color: "#000000"
                text: time
                font.pixelSize: 32
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
                textFormat: Text.RichText
            }






        }

        Rectangle {
            id: tripBox
            x: 134
            y: 300
            width: 737
            height: 185
            color: "#61ffffff"
            radius: 15

            Text {
                id: tripInfoText
                x: 8
                y: 8
                width: 721
                height: 24
                text: "Trip Info"
                font.pixelSize: 19
                horizontalAlignment: Text.AlignHCenter
                textFormat: Text.RichText
            }

            Image {
                id: image1
                x: 84
                y: 44
                width: 77
                height: 53
                source: "img/" + tripImage[0]
                sourceSize.height: 52
                sourceSize.width: 177
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: image2
                x: 345
                y: 44
                width: 40
                height: 53
                source: "img/" + tripImage[1]
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: image3
                x: 572
                y: 44
                width: 81
                height: 53
                source: "img/" + tripImage[2]
                fillMode: Image.PreserveAspectFit
            }

            Text {
                id: text9
                x: 41
                y: 110
                width: 162
                height: 24
                text: tripInfo[0]
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
                textFormat: Text.RichText
                font.bold: true
            }

            Text {
                id: text10
                x: 282
                y: 110
                width: 165
                height: 24
                text: tripInfo[1]
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
            }

            Text {
                id: text11
                x: 532
                y: 110
                width: 162
                height: 24
                text: tripInfo[2]
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
                textFormat: Text.RichText
                font.bold: true
            }

            Text {
                id: text1
                x: 282
                y: 135
                width: 165
                height: 22
                text: "l/100"
                font.pixelSize: 18
                horizontalAlignment: Text.AlignHCenter

            }

            Text {
                id: text2
                x: 41
                y: 135
                width: 162
                height: 22
                text: "Km"
                font.pixelSize: 18
                horizontalAlignment: Text.AlignHCenter
            }

            Text {
                id: text3
                x: 532
                y: 135
                width: 162
                height: 22
                text: "Km"
                font.pixelSize: 18
                horizontalAlignment: Text.AlignHCenter
            }
        }

        Rectangle {
            id: rectangle3
            x: 187
            y: 519
            width: 645
            height: 29
            color: "#61ffffff"
            radius: 15
            visible: isVolumeChanging

            Rectangle {
                id: rectangle4
                x: 0
                y: 0
                width: volume * 21.5
                height: 29
                color: "#ffffff"
                radius: 14.5
            }

            Text {
                id: text12
                x: 316
                y: 8
                width: 14
                height: 13
                text: volume
                font.pixelSize: 12
                fontSizeMode: Text.VerticalFit
                minimumPointSize: 9
                minimumPixelSize: 20
                textFormat: Text.RichText
            }


        }

        GaussianBlur {
            anchors.fill: rectangleBack
            source: rectangleBack
            _color: "#00000000"
            _alphaOnly: false
            radius: 8
            samples: 16
            deviation: 4
            visible: false
        }

        Rectangle {
            id: dark
            x: -10
            y: -9
            width: 1024
            height: 601
            color: "#000000"
            visible: darkMode
        }

        Rectangle {
            id: audioSettingsBox
            x: 152
            y: 69
            width: 700
            height: 446
            color: "#eaeaea"
            radius: 15
            visible: showAudioMenu
            opacity: 0.9


            Text {
                id: audioSettingsMenu
                x: 296
                y: 8
                text: "Audio Settings"
                font.pixelSize: 16
            }

            Rectangle {
                id: bassSlide
                x: 46
                y: 63
                width: 482
                height: 26
                color: "#ffffff"
                radius: 13
            }

            Text {
                id: bassMenu
                x: 46
                y: 33
                width: 482
                height: 24
                text: "Bass"
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
            }




            Rectangle {
                id: bassSlideAct
                x: (bassValue >= 0) ? 262 : 262 - ((Math.abs(bassValue)) * 24)
                y: 63
                width: 50 + ((Math.abs(bassValue)) * 24)
                height: 26
                color: colorVal
                radius: 13
                opacity: (isBass) ? 1 : 0.5
            }

            Text {
                id: trebleMenu
                x: 46
                y: 105
                width: 482
                height: 24
                text: "Treble"
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                id: trebleSlide
                x: 46
                y: 135
                width: 482
                height: 26
                color: "#ffffff"
                radius: 13
            }

            Rectangle {
                id: trebleSlideAct
                x: (trebleValue >= 0) ? 262 : 262 - ((Math.abs(trebleValue)) * 24)
                y: 135
                width: 50 + ((Math.abs(trebleValue)) * 24)
                height: 26
                color: colorVal
                radius: 13
                opacity: (isTreble) ? 1 : 0.5
            }

            Text {
                id: balanceText
                x: 46
                y: 190
                width: 608
                height: 24
                text: "Balance"
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                id: lrBalSlide
                x: 46
                y: 239
                width: 608
                height: 26
                color: "#ffffff"
                radius: 13
            }

            Rectangle {
                id: frBalSlide
                x: 46
                y: 289
                width: 608
                height: 26
                color: "#ffffff"
                radius: 13
            }


            Rectangle {
                id: lrSlideAct
                x: (lrValue >= 0) ? 325 : 325 - ((Math.abs(lrValue)) * 31)
                y: 239
                width: 50 + ((Math.abs(lrValue)) * 31)
                height: 26
                color: colorVal
                radius: 13
                opacity: (isLRBal) ? 1 : 0.5
            }

            Rectangle {
                id: frSlideAct
                x: (rfValue >= 0) ? 325 : 325 - ((Math.abs(rfValue)) * 31)
                y: 289
                width: 50 + ((Math.abs(rfValue)) * 31)
                height: 26
                color: colorVal
                radius: 13
                opacity: (isRFBal) ? 1 : 0.5
            }

            Text {
                id: leftText
                x: 46
                y: 214
                text: "Left"
                font.pixelSize: 16
            }

            Text {
                id: rightText
                x: 612
                y: 214
                text: "Right"
                font.pixelSize: 16
            }

            Text {
                id: rearText
                x: 46
                y: 321
                text: "Rear"
                font.pixelSize: 16
            }

            Text {
                id: frontText
                x: 615
                y: 321
                text: "Front"
                font.pixelSize: 16
            }


            Rectangle {
                id: loudSelect
                x: 550
                y: 79
                width: 120
                height: 26
                color: colorVal
                radius: 13
                opacity: 0.4
                visible: isLoudness

            }

            Rectangle {
                id: autoSelect
                x: 134
                y: 358
                width: 145
                height: 26
                color: colorVal
                radius: 13
                opacity: 0.4
                visible: isAutoVol
            }

            Rectangle {
                id: presetSelect
                x: 446
                y: 358
                width: 113
                height: 26
                color: colorVal
                radius: 13
                opacity: 0.4
                visible: isEQPreset
            }

            Text {
                id: loudText
                x: 569
                y: 80
                text: "Loudness"
                font.pixelSize: 20
            }
            Text {
                id: autoVolText
                x: 149
                y: 358
                text: "Auto Volume"
                font.pixelSize: 20
            }

            Text {
                id: loudStatText
                x: 569
                y: 110
                width: 83
                height: 19
                text: (loudValue == "1") ? "On" : "Off"
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter
            }

            Text {
                id: autoVolStatText
                x: 149
                y: 397
                width: 114
                height: 19
                text: (autoVolValue == "111") ? "On" : "Off"
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter
            }

            Text {
                id: musicAmbText
                x: 459
                y: 358
                text: "EQ Preset"
                font.pixelSize: 20
            }

            Text {
                id: musicAmbPreset
                x: 459
                y: 397
                width: 87
                height: 19
                text: eqPresetValue
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter
            }




        }

        Rectangle {
            id: mainMenuBox
            x: 151
            y: 76
            width: 700
            height: 446
            opacity: 0.9
            visible: showMainMenu
            color: "#eaeaea"
            radius: 15
        }
        DropShadow {
            opacity: 0.5
            anchors.fill: listBox
            horizontalOffset: 3
            verticalOffset: 3
            radius: 8.0
            samples: 17
            color: "#80000000"
            source: listBox
            visible: isListVisible
        }


        Rectangle {
            id: listBox
            x: 222
            y: 160
            width: 559
            height: 264
            color: "#e6ffffff"
            radius: 15
            visible: isListVisible

            Text {
                id: listText
                x: 78
                y: 8
                width: 404
                height: 21
                text: "List"
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                id: selOne
                x: 78
                y: 62
                width: 404
                height: 35
                color: colorVal
                radius: 12
                opacity: (trackListSel[0]) ? 0.4 : 0
            }

            Text {
                id: trackOne
                x: 78
                y: 65
                width: 404
                text: trackList[0]
                font.pixelSize: 24
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                id: selTwo
                x: 78
                y: 103
                width: 404
                height: 35
                color: colorVal
                radius: 12
                opacity: (trackListSel[1]) ? 0.4 : 0
            }

            Text {
                id: trackTwo
                x: 78
                y: 106
                width: 404
                text: trackList[1]
                font.pixelSize: 24
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                id: selThree
                x: 78
                y: 144
                width: 404
                height: 35
                color: colorVal
                radius: 12
                opacity: (trackListSel[2]) ? 0.4 : 0
            }

            Text {
                id: trackThree
                x: 78
                y: 147
                width: 404
                text: trackList[2]
                font.pixelSize: 24
                horizontalAlignment: Text.AlignHCenter
            }

            Rectangle {
                id: selFour
                x: 78
                y: 185
                width: 404
                height: 35
                color: colorVal
                radius: 12
                opacity: (trackListSel[3]) ? 0.4 : 0
            }

            Text {
                id: trackFour
                x: 78
                y: 188
                width: 404
                text: trackList[3]
                font.pixelSize: 24
                horizontalAlignment: Text.AlignHCenter
            }




        }








    }

}
