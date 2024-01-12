import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.2

import "./const/Colors.js" as Colors


APopup {
    id: root
    headerText: "Downloading ..."

    property real maxItemsCount: 0
    property real progressValue: 0

    signal terminateDownload()

    contentItem: Item {
        id: content
        implicitWidth: 200
        implicitHeight: 100

        ColumnLayout {
            id: contentLA
            anchors.fill: parent

            ProgressBar {
                id: progressBar
                from: 0
                to: maxItemsCount
                value: progressValue
                Layout.fillWidth: true
                Layout.preferredHeight: 50
            }

            Button {
                id: cancelBtn
                implicitWidth: 75
                implicitHeight: 30
                text: "Cancel"
                Layout.alignment: Qt.AlignRight | Qt.AlignBottom

                onClicked: {
                    terminateDownload()
//                    close()
                }
            }
        }
    }

    onClosed: {
        progressValue = 0
    }
}