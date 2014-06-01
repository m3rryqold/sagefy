$ = require('jquery')
Bb = require('backbone')
_ = require('underscore')
layoutTemplate = require('../../templates/components/menu/layout')
itemTemplate = require('../../templates/components/menu/item')

class MenuView extends Bb.View
    $body: $('body')
    $page: $('.page')
    className: 'menu'
    events: {
        'click .menu__overlay': 'toggle'
        'click .menu__trigger': 'toggle'
        'click .menu__item a': 'select'
    }

    layoutTemplate: layoutTemplate
    itemTemplate: itemTemplate
    selected: false

    initialize: (options) ->
        @model ||= options.model
        @listenTo(@model, 'changeState', @render)
        @render()

    render: ->
        if ! @$layout
            @_renderLayout()
        @_renderItems()

    _renderLayout: ->
        @$el.html(@layoutTemplate())
        @$items = @$el.find('.menu__items')
        @$body.prepend(@$el)

    _renderItems: ->
        html = _.reduce(@model.items(), (memo, item) =>
            return memo + @itemTemplate(item)
        , '')

        @$items.html(html)

    toggle: (e) ->
        if e
            e.preventDefault()
            e.stopPropagation()
        @selected = ! @selected
        @$el.toggleClass('selected', @selected)

    select: (e) ->
        @$page.empty()
        @toggle()

module.exports = MenuView
