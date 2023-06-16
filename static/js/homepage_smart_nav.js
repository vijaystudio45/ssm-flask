$(document).ready(function () {
    console.log("smart navbar loaded")
});


function switchPromo(media) {
    if (media == 'instagram') {
        $("#promo-title").text("Instagram SSM Tools")
        $("#promo-text").html("Instagram is one of the biggest social media platforms out there. We provide various services for Instagram. <br></br> Our smm tools will improve not only follower counts, but it will increase your social image. Instagram followers and other engagement plays a big role when companies are looking at your profile.");
        $("#buy-followers-btn").attr("href", "https://boostgram.net/add_order/search/Instagram%20|%20Followers|%20Refill");
        $("#buy-comments-btn").attr("href", "https://boostgram.net/add_order/search/Instagram%20|%20Comment%20(Random");
        $("#buy-likes-btn").attr("href", "https://boostgram.net/add_order/Instagram/Instagram%20|%20Likes%20|%20Refill/details");
    }
    else if (media == 'facebook') {
        $("#promo-title").text("Facebook SSM Tools")
        $("#promo-text").html("Facebook is one of the biggest social media platforms out there. We provide various services for Facebook. <br></br> Our smm tools will improve not only follower counts, but it will increase your social image. Facebook followers and other engagement plays a big role when companies are looking at your profile.");
        $("#buy-followers-btn").attr("href", "https://boostgram.net/add_order/search/Facebook%20%20Friend%20Request");
        $("#buy-comments-btn").attr("href", "https://boostgram.net/add_order/search/Facebook%20%20Comments");
        $("#buy-likes-btn").attr("href", "https://boostgram.net/add_order/search/Facebook%20%20Post%20Likes");
    }
    else if (media == 'twitter') {
        $("#promo-title").text("Twitter SSM Tools")
        $("#promo-text").html("Twitter is one of the biggest social media platforms out there. We provide various services for Twitter. <br></br> Our smm tools will improve not only follower counts, but it will increase your social image. Twitter followers and other engagement plays a big role when companies are looking at your profile.");
        $("#buy-followers-btn").attr("href", "https://boostgram.net/add_order/search/Twitter%20|%20Followers");
        $("#buy-comments-btn").attr("href", "https://boostgram.net/add_order/search/Twitter%20|%20Comments");
        $("#buy-likes-btn").attr("href", "https://boostgram.net/add_order/Twitter/Twitter%20|%20Like/details");
    }
    else if (media == 'youtube') {
        $("#promo-title").text("Youtube SSM Tools")
        $("#promo-text").html("Youtube is one of the biggest social media platforms out there. We provide various services for Youtube. <br></br> Our smm tools will improve not only follower counts, but it will increase your social image. Youtube followers and other engagement plays a big role when companies are looking at your profile.");
        $("#buy-followers-btn").attr("href", "https://boostgram.net/add_order/search/YouTube%20%20Subscribers");
        $("#buy-comments-btn").attr("href", "https://boostgram.net/add_order/search/YouTube%20|%20Comments%20|%20Shares");
        $("#buy-likes-btn").attr("href", "https://boostgram.net/add_order/search/YouTube%20|%20Like%20|%20DisLike");
    }
}