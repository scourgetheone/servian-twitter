import React from 'react';
import Tweet from './Tweet';
import { render, unmountComponentAtNode } from 'react-dom';
import { act } from "react-dom/test-utils";


function flushPromises() {
    return new Promise(resolve => setImmediate(resolve));
}

describe('Body', () => {
    let container = null;
    beforeEach(() => {
        // setup a DOM element as a render target
        container = document.createElement("div");
        document.body.appendChild(container);
    });

    afterEach(() => {
        // cleanup on exiting
        unmountComponentAtNode(container);
        container.remove();
        container = null;
    });


    const mockData = {
        avatar_color_index: 3,
        created_at: '2020-02-29T05:30:30.000Z',
        hashtags: '',
        id: '1233625569742348288',
        text: 'test text 2',
        user: 'testuser',
        user_loc: null
    }

    const getUserAbbreviation = (userName) => {
        const names = userName.split('_');

        if (names.length == 1) {
            return names[0].substring(0,2).toUpperCase();
        }

        let abbreviation = '';

        names.slice(0,2).forEach(name => {
            abbreviation += name.charAt(0);
        });

        return abbreviation.toUpperCase();
    };

    it('should display mock tweet header', () => {
        act(() => {
            render(<Tweet tweetData={mockData}/>, container);
        });

        let createdAtDate = new Date(mockData.created_at);
        createdAtDate = createdAtDate.toString().split('GMT')[0];

        const tweetHeader = `On ${createdAtDate} from
        ${mockData.user_loc || 'an unknown location'}, ${mockData.user} wrote`;

        expect(container.querySelectorAll('p')[0].textContent)
        .toBe(tweetHeader);
    });

    it('should display mock tweet text', () => {
        act(() => {
            render(<Tweet tweetData={mockData}/>, container);
        });
        expect(container.querySelectorAll('p')[1].textContent)
        .toBe(mockData.text);
    });

    it('should abbreviate user\'s name', () => {
        act(() => {
            render(<Tweet tweetData={mockData}/>, container);
        });
        expect(container.querySelector('div.MuiAvatar-root').textContent)
        .toBe(getUserAbbreviation(mockData.user));
    });

});
