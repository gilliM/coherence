# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Yield
                                 A QGIS plugin
 prototype fore database connection and coherence between plugin and database
                             -------------------
        begin                : 2014-08-27
        copyright            : (C) 2014 by gillian
        email                : gillian.milani@romandie.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load JamResampler class from file JamResampler.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from yieldProject import yieldMain
    return yieldMain(iface)
