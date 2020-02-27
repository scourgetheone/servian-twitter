import { makeStyles } from '@material-ui/core/styles';
import {
    deepOrange,
    deepPurple,
    pink,
    red,
    blue,
    teal,
    green,
    lime,
    yellow,
    brown,
    grey,
    blueGrey,
    cyan
} from '@material-ui/core/colors';

export default makeStyles(theme => ({
    tweetText: {
        cursor: 'pointer',
    },
    userName: {
        cursor: 'pointer',
        'font-weight': 'bold',
    },
    avatar: {
        width: theme.spacing(8),
        height: theme.spacing(8),
        cursor: 'pointer',
    },
    paper: {
        padding: theme.spacing(2),
        color: theme.palette.text.secondary,
    },
    white: {
        backgroundColor: 'white',
    },
    newTweet: {
        backgroundColor: blue[50],
    },
    orange: {
        color: theme.palette.getContrastText(deepOrange[500]),
        backgroundColor: deepOrange[500],
    },
    purple: {
        color: theme.palette.getContrastText(deepPurple[500]),
        backgroundColor: deepPurple[500],
    },
    pink: {
        color: theme.palette.getContrastText(pink[400]),
        backgroundColor: pink[400],
    },
    red: {
        color: theme.palette.getContrastText(red[400]),
        backgroundColor: red[400],
    },
    blue: {
        color: theme.palette.getContrastText(blue[400]),
        backgroundColor: blue[400],
    },
    teal: {
        color: theme.palette.getContrastText(teal[400]),
        backgroundColor: teal[400],
    },
    green: {
        color: theme.palette.getContrastText(green[400]),
        backgroundColor: green[400],
    },
    lime: {
        color: theme.palette.getContrastText(lime[400]),
        backgroundColor: lime[400],
    },
    yellow: {
        color: theme.palette.getContrastText(yellow[400]),
        backgroundColor: yellow[400],
    },
    brown: {
        color: theme.palette.getContrastText(brown[400]),
        backgroundColor: brown[400],
    },
    grey: {
        color: theme.palette.getContrastText(grey[400]),
        backgroundColor: grey[400],
    },
    blueGrey: {
        color: theme.palette.getContrastText(blueGrey[400]),
        backgroundColor: blueGrey[400],
    },
    cyan: {
        color: theme.palette.getContrastText(cyan[400]),
        backgroundColor: cyan[400],
    }
}));
