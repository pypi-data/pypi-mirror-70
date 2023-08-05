import $ from 'jquery';
import _ from 'underscore';

import { restRequest } from '@girder/core/rest';
import { wrap } from '@girder/core/utilities/PluginUtils';
import ItemListWidget from '@girder/core/views/widgets/ItemListWidget';

import largeImageAnnotationConfig from './configView';

import '../stylesheets/itemList.styl';

wrap(ItemListWidget, 'render', function (render) {
    render.apply(this, _.rest(arguments));

    function addLargeImageAnnotationBadge(item, parent) {
        restRequest({
            type: 'GET',
            url: 'annotation',
            data: {
                itemId: item.id,
                limit: -1
            },
            error: null
        }).done((result, status, jqxhr) => {
            const numAnnotations = +jqxhr.getResponseHeader('Girder-Total-Count') || 0;
            const thumbnail = $('a[g-item-cid="' + item.cid + '"] .large_image_thumbnail', parent).first();

            let badge = thumbnail.find('.large_image_annotation_badge');
            if (badge.length === 0) {
                badge = $(`<div class="large_image_annotation_badge"></div>`).appendTo(thumbnail);
            }
            // update badge
            badge
                .attr('title', `${numAnnotations} annotation${numAnnotations === 1 ? '' : 's'}`)
                .text(numAnnotations)
                .toggleClass('hidden', numAnnotations === 0);
        });
    }

    largeImageAnnotationConfig.getSettings((settings) => {
        // don't render or already rendered
        if (settings['large_image.show_thumbnails'] === false || this.$('.large_image_annotation_badge').length > 0) {
            return;
        }
        const items = this.collection.toArray();
        const parent = this.$el;
        const hasAnyLargeImage = _.some(items, (item) => item.has('largeImage'));

        if (!hasAnyLargeImage) {
            return;
        }

        _.each(items, (item) => {
            if (item.get('largeImage')) {
                item.getAccessLevel(function () {
                    addLargeImageAnnotationBadge(item, parent);
                });
            }
        });
    });
});

export default ItemListWidget;
