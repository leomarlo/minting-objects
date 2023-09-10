import React, { useState, useEffect } from 'react';
import { BACKEND_URL } from '../../utils/global';

function Article() {
  const [article, setArticle] = useState('');

  useEffect(() => {
    const artcle_url = BACKEND_URL + 'get-article';
    console.log('Fetching article from:', artcle_url);
    fetch(artcle_url)
      .then((response) => response.json())
      .then((data) => setArticle(data.articleContent))
      .catch((err) => console.error('Error fetching article:', err));
  }, []);

  return <div>{article}</div>;
}

export default Article;
