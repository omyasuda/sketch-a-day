
void setup() {
  size(500, 500);
  generateVoronoiDiagram(width, height, 25);
  saveFrame("VoronoiDiagram.png");
}

void generateVoronoiDiagram(int w, int h, int num_cells) {
  int nx[] = new int[num_cells];
  int ny[] = new int[num_cells];
  int nr[] = new int[num_cells];
  int ng[] = new int[num_cells];
  int nb[] = new int[num_cells];
  for (int n=0; n < num_cells; n++) {
    nx[n]=int(random(w));
    ny[n]=int(random(h));
    nr[n]=int(random(256));
    ng[n]=int(random(256));
    nb[n]=int(random(256));
    for (int y = 0; y < h; y++) {
      for (int x = 0; x < w; x++) {
        float dmin = dist(0, 0, w - 1, h - 1);
        int j = -1;
        for (int i=0; i < num_cells; i++) {
          float d = dist(0, 0, nx[i] - x, ny[i] - y);
          if (d < dmin) {
            dmin = d;
            j = i;
          }
        }
        set(x, y, color(nr[j], ng[j], nb[j]));
      }
    }
  }
}
