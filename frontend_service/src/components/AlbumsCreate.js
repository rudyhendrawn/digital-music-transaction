import { Wrapper } from "./Wrapper";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const AlbumsCreate = () => {
	const [title, setTitle] = useState('');
	const [artistid, setArtistid] = useState('');
	const navigate = useNavigate();

	const submit = async e => {
		e.preventDefault();

		await fetch('http://localhost:8001/album', {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify({title, artistid})
		});

		await navigate(-1);
	};
	
	return (
		<Wrapper>
			<form className="mt-3">
				<div className="form-floating pb-3">
					<input type="text" className="form-control" id="title" placeholder="Title"></input>
					<label for="title">Title</label>
					<input type="text" className="form-control" id="artistid" placeholder="Artist ID"></input>
					<label for="artistid">Artist ID</label>
				</div>
				<button type="submit" className="btn btn-primary">Submit</button>
			</form>
		</Wrapper>
	);
};