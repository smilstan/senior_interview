import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.2


Popup {
    id: root
    implicitWidth: 200
    implicitHeight: 100
    modal: true
    closePolicy: Popup.NoAutoClose
    anchors.centerIn: parent


    contentItem: Item {
        id: content
        anchors.fill: parent
    }
}