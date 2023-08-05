# -*- coding: UTF-8 -*-
from datetime import datetime
from six import StringIO
from plone import api
from Products.Five.browser import BrowserView

import csv


class ExportUsers(BrowserView):
    """Export the users"""

    def __call__(self):
        mtool = api.portal.get_tool("portal_membership")
        members = mtool.listMembers()
        headers = [u"Name", u"Email"]
        data = []
        for member in members:
            info = {
                u"Name": member.getProperty("fullname", ""),
                u"Email": member.getProperty("email", ""),
            }
            data.append(info)

        out = StringIO()
        writer = csv.DictWriter(out, headers)
        writer.writerow(dict(zip(headers, headers)))
        writer.writerows(data)

        now = datetime.now().strftime("%Y-%m-%d-%H_%M_%s")
        filename = "export-users-%s.csv" % now
        self.request.response.setHeader(
            "Content-Disposition", "attachment; Filename=%s" % filename
        )
        self.request.response.setHeader("Content-type", "text/csv")
        return out.getvalue()
