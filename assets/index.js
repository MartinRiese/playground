import _ from 'underscore';
import $ from 'jquery';
import { View} from "backbone.marionette";

const FormView = View.extend({
    el:'#there',
    template: _.template(`
        <form id="urlForm">
            <label for="url">URL:</label>
            <input type="text" id="url" name="url">
            <input type="submit" value="Submit">
        </form>
        <div id="result"></div>
    `),

    events: {
        'submit #urlForm': 'handleSubmit'
    },

    handleSubmit: function(e) {
        e.preventDefault();
        const url = this.$el.find('#url').val();
        this.sendRequest(url);
    },

    sendRequest: function(url) {
        const self = this;
        $.ajax({
            url: '', // make sure to replace this with your endpoint
            method: 'POST',
            data: url
        }).done(function(response) {
            self.showResponse(response.hash);
        }).fail(function(jqXHR, textStatus) {
            console.log('Request failed: ' + textStatus);
        });
    },

    showResponse: function(hash) {
        this.$el.find('#result').html(hash);
    }
});

const myView = new FormView();
myView.render();
