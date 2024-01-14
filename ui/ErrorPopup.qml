import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.2

import "./const/Colors.js" as Colors


APopup {
    id: root
    headerText: "Error"
    closePolicy: Popup.CloseOnPressOutside

    function init(errorMsg) {
        errorTxt.text = errorMsg
        open()
    }

    contentItem: Item {
        id: content
        implicitWidth: 200
        implicitHeight: 100

        Text {
            id: errorTxt
            anchors.fill: parent
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
}