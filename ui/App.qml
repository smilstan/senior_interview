import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Window 2.13

import "./const/Colors.js" as Colors


ApplicationWindow {
    id: application

    width: 700
    height: 500

    title: "Client App"
    visible: true

    background: Rectangle {
        id: background
        anchors.fill: parent
        color: Colors.dark
    }

    GridView {
        id: gridView
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
    }

    DownloadProgressPopup {
        id: downloadProgressPopup
        maxItemsCount: client ? client.getMaxItemsCount() : 0

        onTerminateDownload: {
            client.terminateModelSetup()
        }
    }

    Connections {
        target: client
        onModelChanged: {
            downloadProgressPopup.progressValue = client.model.length
        }

        onDownloadStateChanged: {
            if ( client.downloadState ) {
                downloadProgressPopup.open()
            } else {
                downloadProgressPopup.close()
            }
        }
    }
}