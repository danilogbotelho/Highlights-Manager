Introduction
============

Almost every site has one or more areas in it's homepage to highlight news or other content.
Some efforts have been made to provide the viewlets for those highlights but Plone does not have
the mechanism to manage wich items go where and when builtin.

collective.hightlights.manager allows for a site administrator (or contributor with permission) to mark content to
appear at highlight sections and to configure the information that will be presented.

Thus, one can count on a single product to manage the highlighted content they will show and administrators
don't need to reconfigure every product to display their content every time they change from 
'caroussel' to 'easy slider' or anything else.


TODO
=====

1. Allow administrator to protect item/group assignment with permissions (by user/role, by path, by content type etc.)
2. Create workflow state for items. Group policy defines which will aply: 
    a) Highlight State: Hidden, Visible
    b) Highlight State: Private, Pending review, Visible, Hidden

Installation
============

collective.highlights.manager depends on plone.app.z3cform package
which needs a few version pins for Plone 3.x:::

	[buildout]

	...

	versions = versions

	[versions]
	z3c.form = 1.9.0
	zope.i18n = 3.4.0
	zope.testing = 3.4.0
	zope.component = 3.4.0
	zope.securitypolicy = 3.4.0
	zope.app.zcmlfiles = 3.4.3

After certifying that dependencies will be met, just add it to your buildout:::

	[buildout]

	...

	eggs = 
		collective.highlights.manager

	zcml = 
		collective.highlights.manager
