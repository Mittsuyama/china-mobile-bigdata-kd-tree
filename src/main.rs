use std::fs;
use std::io::Write;
use kd_tree::{KdPoint, KdTree};
use typenum;
use indicatif::{ProgressBar, ProgressStyle};

struct Poi {
    id: u64,
    point: [f64; 2],
}

struct Cell {
    id: String,
    point: [f64; 2],
}

impl KdPoint for Poi {
    type Scalar = f64;
    type Dim = typenum::U2;
    fn at(&self, k: usize) -> f64 { self.point[k] }
}

fn check_position(lng: f64, lat: f64) -> bool {
    if lng > 126.48
    && lng < 126.83
    && lat > 45.64
    && lat < 45.86 {
        true
    } else {
        false
    }
}

fn main() {
    println!("reading poi file...");

    let poi_content = fs::read_to_string("data/poi.txt").unwrap();
    let lines: Vec<&str> = poi_content.split("\n").collect();
    let mut poi_list: Vec<Poi> = vec![];
    let mut count = 0u64;
    for line in lines {
        count += 1;
        let split_reuslt: Vec<&str> = line.split(",").collect();
        if split_reuslt.len() < 6 {
            continue;
        }
        if let (Ok(lng), Ok(lat))
            = (split_reuslt[5].parse::<f64>(), split_reuslt[6].parse::<f64>()) {
                if !check_position(lng, lat) {
                    continue;
                }
                poi_list.push(Poi {
                    id: count,
                    point: [lng, lat],
                });
        }
    }

    println!("building tree...");
    let tree: KdTree<Poi> = KdTree::build_by_ordered_float(poi_list);

    println!("reading cell file...");
    let cell_content = fs::read_to_string("data/cell.txt").unwrap();
    let lines: Vec<&str> = cell_content.split("\n").collect();
    let mut cell_list: Vec<Cell> = vec![];
    for line in lines {
        let split_reuslt: Vec<&str> = line.split(",").collect();
        if split_reuslt.len() < 14 {
            continue;
        }
        if let (Ok(lng), Ok(lat))
            = (split_reuslt[12].parse::<f64>(), split_reuslt[13].parse::<f64>()) {
                if !check_position(lng, lat) {
                    continue;
                }
                cell_list.push(Cell {
                    id: split_reuslt[14].to_owned(),
                    point: [lng, lat],
                });
            }
    }
    let bar = ProgressBar::new(cell_list.len() as u64);
    bar.set_style(ProgressStyle::default_bar()
        .template("[{elapsed_precise}] {bar:60.cyan/blue} {pos:>7}/{len:7} {msg}")
        .progress_chars("##-"));

    println!("getting latest poi...");
    let mut out_file = fs::File::create("data/nearst.txt").unwrap();
    for cell in cell_list {
        let poi_id = &tree.nearest(&cell.point).unwrap().item.id;
        out_file.write(format!("{},{}\n", cell.id, poi_id).as_ref()).unwrap();
        bar.inc(1);
    }
}
