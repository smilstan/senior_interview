import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Window 2.13

import "./const/Colors.js" as Colors


ApplicationWindow {
    id: application

    width: 720
    height: 480

    title: "Client App"
    visible: true

    background: Rectangle {
        id: background
        anchors.fill: parent
        color: Colors.dark
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
    }

    DownloadProgressPopup {
        id: downloadProgressPopup
        maxItemsCount: client.getMaxItemsCount()

        onTerminateDownload: {
            client.terminateDownloadProcess()
        }
    }

    Connections {
        target: client
        onModelChanged: {
            downloadProgressPopup.progressValue = client.model.length
        }

        onDownloadStateChanged: {
            print(client.downloadState)
            if ( client.downloadState ) {
                downloadProgressPopup.open()
            } else {
                downloadProgressPopup.close()
            }
        }
    }
}