function like(postId){
    const likeCount=document.getElementById(`likes-count-${postId}`).innerHTML;
    const likeButton=document.getElementById(`like-button-${postId}`);
    console.log(likeCount);
    console.log(likeButton);
}