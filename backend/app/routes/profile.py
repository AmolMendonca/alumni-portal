# app/routes/profile.py
from app.services.vector import VectorService
from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from bson import Binary
from bson import ObjectId
from app.services.profile import ProfileService
from app.models.profile import AlumniProfile
from app.utils.validation import validate_profile_data
from pydantic import HttpUrl



def create_profile_blueprint(database):
    
    profile_bp = Blueprint('profile', __name__)
    
    profile_service = ProfileService(database)
    
    vector_service = VectorService()
    
    @profile_bp.route('/', methods=['POST'])
    #@require_auth
    async def create_profile():
        """
        Create new alumni profile
        
        Request body:
        {
            "fullName": "Jane Smith",
            "currentRole": "Software Engineer",
            "company": "Tech Innovations",
            "university": "UC Berkeley",
            "highSchool": "Oakridge High",
            "linkedInURL": "https://linkedin.com/in/janesmith"
        }
        """
        try:
            data = request.get_json()
            
            # Validate profile data
            validation_result = validate_profile_data(data)
            if not validation_result['valid']:
                return jsonify({
                    "status": "error",
                    "message": validation_result['message']
                }), HTTPStatus.BAD_REQUEST
                
            temp_profile = AlumniProfile(**data)
            
            try:
                vector_embedding = vector_service.generate_profile_vector(temp_profile)
                data['alumniEmb'] = vector_embedding
            except Exception as e:
                current_app.logger.error(f"Error generating vector embedding: {str(e)}")
                return jsonify({
                    "status": "error",
                    "message": "Failed to generate profile embedding"
                }), HTTPStatus.INTERNAL_SERVER_ERROR
                
            # Create profile
            profile = await profile_service.create_profile(data)
            
            return jsonify({
                "status": "success",
                "profile": profile
            }), HTTPStatus.CREATED
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    @profile_bp.route('/get-profile/', methods=['GET'])
    #@require_auth
    def get_profile():
        """
        Get alumni profile by ID

        Request body:
        {
        "profile_id": "6726ac2b41c292327ac3b0a4"
        }
        """
        try:
            data = request.get_json()
            profile_id = data.get('profile_id')
            profile = profile_service.get_profile(profile_id)
            print(profile)
            if not profile:
                return jsonify({
                    "status": "error",
                    "message": "Profile not found"
                }), HTTPStatus.NOT_FOUND
                
            profile_dict = profile.model_dump(by_alias=True)
            for key, value in profile_dict.items():
                if isinstance(value, ObjectId):
                    profile_dict[key] = str(value)
                    
                if isinstance(value, HttpUrl):
                    profile_dict[key] = str(value)
                
            return jsonify({
                "status": "success",
                "profile": profile_dict
            }), HTTPStatus.OK
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    @profile_bp.route('/update-profile/', methods=['PUT'])
    #@require_auth
    async def update_profile(profile_id: str):
        """Update profile by ID"""
        try:
            data = request.get_json()
            profile_id = data.get('profile_id')
            
            # Validate update data
            validation_result = validate_profile_data(data, is_update=True)
            if not validation_result['valid']:
                return jsonify({
                    "status": "error",
                    "message": validation_result['message']
                }), HTTPStatus.BAD_REQUEST
                
            # Update profile
            updated_profile = await profile_service.update_profile(profile_id, data)
            
            if not updated_profile:
                return jsonify({
                    "status": "error",
                    "message": "Profile not found"
                }), HTTPStatus.NOT_FOUND
                
            return jsonify({
                "status": "success",
                "profile": updated_profile.dict(by_alias=True)
            }), HTTPStatus.OK
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    @profile_bp.route('/<profile_id>', methods=['DELETE'])
    #@require_admin
    async def delete_profile(profile_id: str):
        """Delete profile by ID (admin only)"""
        try:
            success = await profile_service.delete_profile(profile_id)
            
            if not success:
                return jsonify({
                    "status": "error",
                    "message": "Profile not found"
                }), HTTPStatus.NOT_FOUND
                
            return jsonify({
                "status": "success",
                "message": "Profile deleted successfully"
            }), HTTPStatus.OK
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    @profile_bp.route('/batch', methods=['POST'])
    #@require_admin
    async def batch_create_profiles():
        """
        Batch create profiles (admin only)
        
        Request body:
        {
            "profiles": [
                {
                    "fullName": "Jane Smith",
                    "currentRole": "Software Engineer",
                    ...
                },
                ...
            ]
        }
        """
        try:
            data = request.get_json()
            profiles_data = data.get('profiles', [])
            
            created_profiles = await profile_service.create_many_profiles(profiles_data)
            
            return jsonify({
                "status": "success",
                "created_count": len(created_profiles),
                "profiles": [p.dict(by_alias=True) for p in created_profiles]
            }), HTTPStatus.CREATED
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR
            
    return profile_bp