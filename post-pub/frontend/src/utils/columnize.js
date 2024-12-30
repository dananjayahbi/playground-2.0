export const splitIntoColumns = (posts, columns = 4) => {
    const columnData = Array.from({ length: columns }, () => []);
    posts.forEach((post, index) => {
      columnData[index % columns].push(post);
    });
    return columnData;
  };
  