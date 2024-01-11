import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.2


Popup {
    id: root
    implicitWidth: 200
    implicitHeight: 100
    modal: true
    closePolicy: Popup.CloseOnPressOutside
    anchors.centerIn: parent

    readonly property alias colorName: textInput.text
    property var objectToChange: null

    function init(itemObject) {
        objectToChange = itemObject
        open()
    }

    contentItem: Item {
        id: content
        anchors.fill: parent

        RowLayout {
            anchors.fill: parent

            Text {
                id: lblTxt
                text: "Color"
            }

            TextInput {
                id: textInput
                width: 50
                height: 30
            }
        }
    }
}