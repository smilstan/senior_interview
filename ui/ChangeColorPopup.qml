import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.2

import "./const/Colors.js" as Colors


APopup {
    id: root
    headerText: "Enter new color"

    property var colorChangeItem: null   // item which color should be changed

    function init(itemObject) {
        colorChangeItem = itemObject
        textInput.text = ""
        open()
    }

    contentItem: Item {
        id: content
        implicitWidth: 200
        implicitHeight: 100

        ColumnLayout {
            id: contentLA
            anchors.fill: parent

            Rectangle {
                width: 150
                height: 30
                border { width: 1 }
                radius: 5
                color: "transparent"
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 5

                TextInput {
                    id: textInput
                    anchors.fill: parent
                    horizontalAlignment: TextInput.AlignHCenter
                    verticalAlignment: TextInput.AlignVCenter
                    maximumLength: 15
                }
            }

            RowLayout {
                id: buttonsLA
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height / 2
                Layout.alignment: Qt.AlignHCenter

                Button {
                    id: cancelBtn
                    implicitWidth: 75
                    implicitHeight: 30
                    text: "Cancel"

                    onClicked: {
                        colorChangeItem = null
                        close()
                    }
                }

                Button {
                    id: okBtn
                    implicitWidth: 75
                    implicitHeight: 30
                    text: "Ok"

                    onClicked: {
                        if ( textInput.text.trim() != "" ) {
                            colorChangeItem.color = textInput.text
                        }
                        close()
                    }
                }
            }
        }
    }
}