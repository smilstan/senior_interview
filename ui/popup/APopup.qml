import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.2

import "../const/Colors.js" as Colors


Popup {
    id: abstractPopup
    modal: true
    closePolicy: Popup.NoAutoClose
    anchors.centerIn: parent
    topPadding: 25
    leftPadding: 10
    rightPadding: 10
    bottomPadding: 10

    property alias headerText: header.text

    background: Rectangle {
        id: background
        color: Colors.white_smoke
        radius: 10
        anchors.fill: parent

        Text {
            id: header
            text: "Header"
            font { pixelSize: 16; bold: true }
            anchors {
                top: parent.top
                horizontalCenter: parent.horizontalCenter
                topMargin: 5
            }
        }
    }
}