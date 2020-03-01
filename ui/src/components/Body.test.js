import React from 'react';
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import Body from './Body';


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

    it('should load tweet data after async fetch', async () => {
        let component;
        const mockData = {
            stream_keyword: "test keyword",
            tweets: [{
                avatar_color_index: 3,
                created_at: '2020-02-29T05:30:30.000Z',
                hashtags: '',
                id: '1233625569742348288',
                text: 'test text',
                user: 'testuser',
                user_loc: null
            }]
        };
        // Issue with using jest.spyOn so had to have this workaround:
        // https://medium.com/@rishabhsrao/mocking-and-testing-fetch-with-jest-c4d670e2e167
        global.fetch = jest.fn().mockImplementation(() => {
            const fetchResponse = {
                json: () => Promise.resolve(mockData)
            };
            return Promise.resolve(fetchResponse);
        });

        await act(async () => {
            render(<Body />, container);
        });

        // Test that the header text displays correctly after async fetching from the backend api
        expect(container.querySelector('h5').textContent)
        .toBe(`Welcome to Servian's real-time Twitter stream, proudly serving you today all things ${mockData.stream_keyword}`);

        // Test that the tweet's text appears in the right place after the async call
        expect(container.querySelectorAll('p')[1].textContent)
        .toBe(mockData.tweets[0].text);

        // Clean up the mock fetch function
        global.fetch.mockClear();
        delete global.fetch;
    });

});
