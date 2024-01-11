import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Window 2.13


ApplicationWindow {
    id: application

    width: 720
    height: 480

    title: "Client App"
    visible: true

    background: Rectangle {
        id: background
        anchors.fill: parent
        color: "#242424"
    }

    GridView {
        id: gridView
        cellWidth: 75
        cellHeight: 75
        anchors.fill: parent

        model: DragDropDelegateModel {
            parentContainer: gridView

            onChangeColorRequest: {
                changeColorPopup.init(itemObject)
            }
        }
    }

    ChangeColorPopup {
        id: changeColorPopup

        onClosed: {
            if ( colorName != "" ) {
                objectToChange.color = colorName
            }
        }
    }
}