import { Wrapper } from "./Wrapper";
import { useState, useEffect} from "react";
import { Link } from "react-router-dom";

export const Albums = () => {
	const [albums, setAlbums] = useState([]);

	useEffect(() => {
		(async () => {
			try {
				const response = await fetch('http://localhost:8000/getalbum');
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				const data = await response.json();
				setAlbums(data);
			} catch (error) {
				console.error("Failed to fetch albums: ", error);
			}
		})(); 
	}, []);

	const del = async id => {
		if (window.confirm('Are you sure you want to delete this record?')) {
			try {
				const response = await fetch('http://localhost:8001/album/' + id, {
					method: 'DELETE'
				});
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				setAlbums(albums.filter(album => album.id !== id));
			} catch (error) {
				console.error("Failed to delete album: ", error);
			}
		}
	};

	return (
		<Wrapper>
			<div className="pt-3 pb-2 mb-3 border-bottom">
				<Link to="/album/create" className="btn btn-sm btn-primary">Add</Link>
			</div>
			<div className="table-responsive small">
				<table className="table table-striped table-sm">
				<thead>
					<tr>
					<th scope="col">#</th>
					<th scope="col">Title</th>
					<th scope="col">Artist ID</th>
					<th scope="col">Actions</th>
					</tr>
				</thead>
				<tbody>
					{albums.map(album => {
						return (
							<tr key={album.id}>
								<td>{album.id}</td>
								<td>{album.title}</td>
								<td>{album.artistid}</td>
								<td>
									<a href="#" class="btn btn-secondary btn-sm">Edit</a>
									<a href="#" class="btn btn-danger btn-sm" onClick={e => del(album.id)}>Delete</a>
								</td>
							</tr>
						);
					})}
				</tbody>
				</table>
			</div>
		</Wrapper>
	);
};