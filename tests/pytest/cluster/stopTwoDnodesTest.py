###################################################################
#           Copyright (c) 2016 by TAOS Technologies, Inc.
#                     All rights reserved.
#
#  This file is proprietary and confidential to TAOS Technologies.
#  No part of this file may be reproduced, stored, transmitted,
#  disclosed or used in any form or by any means other than as
#  expressly provided by the written permission from Jianhui Tao
#
###################################################################

# -*- coding: utf-8 -*-

import sys
from clustertest import *
from util.sql import tdSql
from util.log import tdLog
import random

class ClusterTestcase:
    
    ## test case 17, 18 ##
    def run(self):
        
        nodes = Nodes()
        ctest = ClusterTest(nodes.node1.hostName)
        ctest.connectDB()        
        ctest.createSTable(1)
        ctest.run()
        tdSql.init(ctest.conn.cursor(), False)
        
        tdSql.query("show databases")
        count = tdSql.queryRows;
        tdSql.execute("use %s" % ctest.dbName)
        tdSql.execute("alter database %s replica 3" % ctest.dbName)    
        nodes.node2.stopTaosd()
        nodes.node3.stopTaosd()
        tdSql.error("show databases")
        
        nodes.node2.startTaosd()
        tdSql.error("show databases")

        nodes.node3.startTaosd()
        tdSql.query("show databases")
        tdSql.checkRows(count)
        
ct = ClusterTestcase()
ct.run()
